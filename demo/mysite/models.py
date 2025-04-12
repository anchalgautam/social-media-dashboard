from django.contrib.auth.models import User
from django.db import models

PLATFORM_CHOICES = [
    ('twitter', 'Twitter'),
    ('facebook', 'Facebook'),
    ('both', 'Both'),
]


# 🗨️ Comment Model
class FeedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=10, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter')])
    content = models.TextField()  # the post being commented on
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.platform}"


# ❤️ Like Model with uniqueness
class FeedLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=10)
    content = models.TextField()
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content', 'platform')

    def __str__(self):
        return f"{self.user.username} liked on {self.platform}"


# 📅 Scheduled Post Model
class ScheduledPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | {self.platform} | {self.scheduled_time}"


# 👤 User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    twitter_username = models.CharField(max_length=255, blank=True)
    facebook_username = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
class SocialPost(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
    ]

    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    post_id = models.CharField(max_length=100)
    message = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.post_id}"
