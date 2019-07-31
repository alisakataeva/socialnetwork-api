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


class MakeFriend(GenericAPIView):

    def post(self, request):

        user = request.user
        if user:
            try:
                profile = user.userprofile
            except AttributeError:
                return Response({'message': 'You are not authenticated'})
        else:
            return Response({'message': 'You are not authenticated'})

        try:
            profile2 = UserProfile.objects.get(pk=int(request.POST.get('user_id')))
        except UserProfile.DoesNotExist:
            return Response({'message': 'Error on make user your friend'})

        fs = Friendship.objects.filter(
            Q( id_user1=profile.id, id_user2=profile2.id ) | 
            Q( id_user1=profile2.id, id_user2=profile.id )
        )
        if not fs.exists():
            fs = Friendship.objects.create(
                id_user1=profile.id,
                id_user2=profile2.id,
                relationship='FRIENDS'
            )
            return Response({'message': 'Success'})
        return Response({'message': 'Already friends'})