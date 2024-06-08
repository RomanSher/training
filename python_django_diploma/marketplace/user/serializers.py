from rest_framework import serializers

from project.exceptions import (
    UserPasswordMismatchError, UserIncorrectError, UserOldPasswordError
)
from user.models import User
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise UserPasswordMismatchError

        return attrs

    def create(self, validated_data):
        user = User(
            full_name=self.validated_data['full_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        user = authenticate(**validated_data)
        if user and user.is_active:
            return user
        raise UserIncorrectError


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'avatar')
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.phone = validated_data['phone']
        instance.save()

        return instance


class ProfileAvatarUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.avatar = validated_data['avatar']
        instance.save()

        return instance


class ProfilePasswordUpdateSerializer(serializers.ModelSerializer):
    password_current = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_reply = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password_current', 'password', 'password_reply')

    def validate_password_current(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise UserOldPasswordError
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_reply']:
            raise UserPasswordMismatchError

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
