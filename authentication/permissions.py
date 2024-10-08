from rest_framework import permissions
from .models import User


class IsSameUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj
