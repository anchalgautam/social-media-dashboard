from django.contrib import admin
from .models import SocialPost  # <-- Import model

# Register model to admin
admin.site.register(SocialPost)
