from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.decorators import APIView
from .models import Blog
from .serializers import BlogSerializer
from django.shortcuts import get_object_or_404
from .permissions import AuthorOrReadOnly

# Create your views here.


class BlogPagination(PageNumberPagination):
    page_size = 2


class BlogListAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BlogSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = Blog.objects.order_by('-created_at')

        username = request.query_params.get('username', None)
        search = request.query_params.get('search', None)

        if username is not None:
            queryset = queryset.filter(author__username=username)

        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        paginator = BlogPagination()
        queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(instance=queryset, many=True)

        paginated_response = paginator.get_paginated_response(serializer.data)

        response = {
            "message": "success",
            "data": paginated_response.data
        }

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            response = {
                "message": "successfully created blog",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogRetrieveUpdateDestroyView(APIView):
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = BlogSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        blog = get_object_or_404(Blog, pk=kwargs['blog_id'])
        serializer = self.serializer_class(blog)
        response = {
            "message": "successfully fetched the blog",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs) -> Response:
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_id'])
        self.check_object_permissions(request, blog)
        data = request.data
        serializer = self.serializer_class(instance=blog, data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "successfully updated the blog",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_id'])
        self.check_object_permissions(request, blog)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
