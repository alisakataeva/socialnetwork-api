from rest_framework import routers

from api import views


router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'user_profiles', views.UserProfileViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'friend_relations', views.FriendshipViewSet)