from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.authenticate import IsNotAuthenticated
from user.models import User
from user.serializers import (
    UserRegistrationSerializer, UserLoginSerializer, ProfileUpdateSerializer,
    ProfileAvatarUpdateSerializer, ProfilePasswordUpdateSerializer
)


class UserRegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = User.refresh_token_user(user)
        return Response(token, status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_205_RESET_CONTENT)


class ProfileAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileAvatarAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileAvatarUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfilePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
