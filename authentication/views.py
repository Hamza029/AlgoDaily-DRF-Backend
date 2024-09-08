from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .tokens import create_jwt_pair


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

    def post(self, request: Request, *args, **kwargs) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = create_jwt_pair(user)
            response = {
                "message": "Logged in successfully.",
                "tokens": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
