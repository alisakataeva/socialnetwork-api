from django.contrib import admin
from api.models import UserProfile, Tag, Post, Friendship


# Register your models here.


admin.site.register( UserProfile )
admin.site.register( Tag )
admin.site.register( Post )
admin.site.register( Friendship )