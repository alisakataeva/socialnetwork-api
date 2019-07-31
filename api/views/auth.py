from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import UserProfileSerializer
from api.models import UserProfile


class RegisterView(APIView):

    def post(self, request):
        try:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
            )
            profile = UserProfile.objects.create(
                user=user,
                avatar=request.FILES.get('avatar')
            )
            serializer = UserProfileSerializer(
                profile, context={'request': request})
            return Response({'user': serializer.data})
        except Exception as e:
            return Response({'message': 'Fail to register an user.'})


class LoginView(APIView):

    def post(self, request):
        try:
            user = authenticate(
                request=request,
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )
            if user:
                login( request, user )
                try:
                    profile = user.userprofile
                    serializer = UserProfileSerializer(
                        profile, context={'request': request})
                    return Response({'user': serializer.data})
                except AttributeError:
                    return Response({'message': 'wat'})
            return Response({'message': 'Error on log in'})
        except User.DoesNotExist:
            return Response({'message': 'User dows not exist'})


class LogoutView(APIView):

    def get(self, request):
        logout( request )
        return Response({'message': 'You have successfully logged out.'})