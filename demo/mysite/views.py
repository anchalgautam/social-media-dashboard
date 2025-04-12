from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count, Avg, Sum
import tweepy
import requests

from .models import Profile, ScheduledPost, FeedComment, FeedLike, SocialPost
from .forms import UserForm, ProfileForm, ScheduledPostForm

# ---------------------
# Dashboard View
# ---------------------
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ---------------------
# Edit Profile View
# ---------------------
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# ---------------------
# Twitter Feed View
# ---------------------
@login_required
def twitter_feed(request):
    tweet_data = []
    try:
        client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)
        username = request.user.profile.twitter_username or "TwitterDev"
        user = client.get_user(username=username)
        tweets = client.get_users_tweets(id=user.data.id, max_results=5)
        tweet_data = [tweet.text for tweet in tweets.data] if tweets.data else []
    except Exception as e:
        tweet_data = [f"Twitter Error: {str(e)}"]

    return render(request, 'twitter_feed.html', {'tweets': tweet_data})

# ---------------------
# Facebook Feed View
# ---------------------
@login_required
def facebook_feed(request):
    posts = []
    try:
        url = f"https://graph.facebook.com/me/feed?access_token={settings.FACEBOOK_ACCESS_TOKEN}"
        response = requests.get(url)
        data = response.json()
        posts = [post.get('message', '[No text content]') for post in data.get('data', [])]
    except Exception as e:
        posts = [f"Facebook Error: {str(e)}"]

    return render(request, 'facebook_feed.html', {'posts': posts})

# ---------------------
# Combined Feed View
# ---------------------
@login_required
def combined_feed(request):
    twitter_feed = []
    facebook_feed = []

    try:
        client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)
        username = request.user.profile.twitter_username or 'TwitterDev'
        user = client.get_user(username=username)
        tweets = client.get_users_tweets(id=user.data.id, max_results=5)
        twitter_feed = [tweet.text for tweet in tweets.data] if tweets.data else []
    except Exception as e:
        twitter_feed = [f"Twitter Error: {str(e)}"]

    try:
        url = f"https://graph.facebook.com/me/feed?access_token={settings.FACEBOOK_ACCESS_TOKEN}"
        response = requests.get(url)
        fb_data = response.json()
        facebook_feed = [post.get('message', '[No text content]') for post in fb_data.get('data', [])]
    except Exception as e:
        facebook_feed = [f"Facebook Error: {str(e)}"]

    if request.method == 'POST':
        content = request.POST.get('content')
        platform = request.POST.get('platform')
        comment = request.POST.get('comment')
        like = request.POST.get('like')
        unlike = request.POST.get('unlike')

        if comment:
            FeedComment.objects.create(user=request.user, content=content, platform=platform, comment=comment)
        elif like == '1':
            FeedLike.objects.get_or_create(user=request.user, content=content, platform=platform)
        elif unlike == '1':
            FeedLike.objects.filter(user=request.user, content=content, platform=platform).delete()

    comments = FeedComment.objects.filter(user=request.user).order_by('-created_at')
    likes = FeedLike.objects.filter(user=request.user)
    liked_contents = list(likes.values_list('content', flat=True))

    return render(request, 'combined_feed.html', {
        'twitter_feed': twitter_feed,
        'facebook_feed': facebook_feed,
        'comments': comments,
        'liked_contents': liked_contents,
    })

# ---------------------
# Schedule Post View
# ---------------------
@login_required
def schedule_post(request):
    if request.method == 'POST':
        if 'post_now' in request.POST:
            post_id = request.POST.get('post_id')
            post = ScheduledPost.objects.get(id=post_id, user=request.user)

            if post.platform in ['twitter', 'both']:
                try:
                    client = tweepy.Client(
                        bearer_token=settings.TWITTER_BEARER_TOKEN,
                        consumer_key=settings.TWITTER_API_KEY,
                        consumer_secret=settings.TWITTER_API_SECRET,
                        access_token=settings.TWITTER_ACCESS_TOKEN,
                        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
                    client.create_tweet(text=post.content)
                except Exception as e:
                    print("Twitter Error:", e)

            if post.platform in ['facebook', 'both']:
                try:
                    url = "https://graph.facebook.com/me/feed"
                    payload = {
                        'message': post.content,
                        'access_token': settings.FACEBOOK_ACCESS_TOKEN
                    }
                    requests.post(url, data=payload)
                except Exception as e:
                    print("Facebook Error:", e)

            post.posted = True
            post.save()
            return redirect('schedule_post')

        else:
            form = ScheduledPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('schedule_post')
    else:
        form = ScheduledPostForm()

    user_posts = ScheduledPost.objects.filter(user=request.user).order_by('-scheduled_time')
    return render(request, 'schedule_post.html', {'form': form, 'user_posts': user_posts})

# ---------------------
# Analytics View
# ---------------------
@login_required
def analytics_view(request):
    context = {}
    for platform in ['facebook', 'twitter']:
        posts = SocialPost.objects.filter(platform=platform)
        total_likes = posts.aggregate(Sum('likes'))['likes__sum'] or 0
        total_comments = posts.aggregate(Sum('comments'))['comments__sum'] or 0
        total_shares = posts.aggregate(Sum('shares'))['shares__sum'] or 0
        engagement = round((total_likes + total_comments) / posts.count(), 2) if posts.exists() else 0

        context[platform] = {
            'total_posts': posts.count(),
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'engagement_rate': engagement
        }

    return render(request, 'analytics.html', context)