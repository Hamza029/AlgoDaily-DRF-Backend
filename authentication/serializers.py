from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=45)
    last_name = serializers.CharField(max_length=45)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'password')

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()

        if email_exists:
            raise ValidationError('Email already registered')

        if username_exists:
            raise ValidationError('This username is already taken')

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)  # for hashed password
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
