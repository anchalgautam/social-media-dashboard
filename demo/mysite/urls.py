from django.urls import path
from . import views

urlpatterns = [
    # 📋 Core Dashboard Routes
    path('', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # 📡 Social Feed Views
    path('twitter-feed/', views.twitter_feed, name='twitter_feed'),
    path('facebook-feed/', views.facebook_feed, name='facebook_feed'),
    path('combined-feed/', views.combined_feed, name='combined_feed'),

    # ⏰ Scheduler
    path('schedule-post/', views.schedule_post, name='schedule_post'),
    path('analytics/', views.analytics_view, name='analytics'),

]

