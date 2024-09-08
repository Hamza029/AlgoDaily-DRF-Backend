from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOrCreate(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.method == 'POST'


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author

