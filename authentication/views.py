from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.shortcuts import render
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsSameUserOrReadOnly
from .serializers import SignupSerializer, UserSerializer, LoginSerializer, LogoutSerializer
from rest_framework import generics, status, pagination, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from .tokens import create_jwt_pair
from drf_yasg.utils import swagger_auto_schema


class UsersPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20


class SignupView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Account created successfully.",
                "data": serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = create_jwt_pair(user)
            response = {
                "message": "Logged in successfully.",
                "tokens": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            raise InvalidToken(serializer.errors)
        refresh_token = serializer.data.get('refresh')
        RefreshToken(refresh_token).blacklist()
        response = {
            "message": "Logged out successfully.",
        }
        return Response(data=response, status=status.HTTP_200_OK)


class UserListView(mixins.ListModelMixin ,generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.order_by('-date_joined')
    pagination_class = UsersPagination

    def get_queryset(self):
        queryset = self.queryset.order_by('-date_joined')
        search = self.request.query_params.get('username', None)
        if search is not None:
            queryset = queryset.filter(username__icontains=search)
        return queryset

    @swagger_auto_schema(
        operation_summary="Get users list",
        operation_description='This returns a list of users',
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_QUERY, description="Search by username", type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        generic_response = self.list(request, *args, **kwargs)
        response = {
            "message": "Successfully listed users.",
            "data": generic_response.data
        }
        return Response(data=response, status=status.HTTP_200_OK)


class UserRetrieveUpdateView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = (IsSameUserOrReadOnly, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary="Retrieve a user",
        operation_description='This will retrieve a user from given id parameter',
    )
    def get(self, request, *args, **kwargs):
        generic_response = self.retrieve(request, *args, **kwargs)
        response = {
            "message": "Successfully retrieved user.",
            "data": generic_response.data
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        generic_response = self.update(request, *args, **kwargs)
        response = {
            "message": "Successfully updated user.",
            "data": generic_response.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
