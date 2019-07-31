import json

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import GenericAPIView

from api.models import UserProfile, Post, Friendship
from api.serializers import UserSerializer, UserProfileSerializer, PostSerializer, FriendshipSerializer


class CurrentUserData(GenericAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = UserProfileSerializer

    def get(self, request):
        try:
            profile = request.user.userprofile
            serializer = UserProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)
        except AttributeError:
            return Response({'nodetail': 'Anonymous User'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.GET.get('id'):
            try:
                user_id = int( request.GET.get('id') )
                friends_relationships = Friendship.objects.filter(
                    Q( id_user1=user_id ) | Q( id_user2=user_id ), relationship='FRIENDS')
                friends_ids = [ f.id_user1 if f.id_user2 == user_id else f.id_user2 for f in friends_relationships ]

                queryset = queryset.filter( id__in=friends_ids )
            except ValueError:
                pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.GET.get('id'):
            user_id = int( request.GET.get('id') )
            queryset = queryset.filter( author__id=user_id )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer