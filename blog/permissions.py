from rest_framework.permissions import BasePermission, SAFE_METHODS
from blog.models import Blog


class ReadOrCreate(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.method == 'POST'


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj: Blog):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author

