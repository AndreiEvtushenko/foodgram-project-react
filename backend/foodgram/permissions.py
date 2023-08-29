from rest_framework import permissions


class ChangeObjectIfAuthorOrAdmin(permissions.BasePermission):
    """
    Custom permission class:
    GET requests are allowed for everyone.
    POST, PATCH, DELETE requests are only allowed for authenticated users
    and object authors.
    All actions are allowed for admin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and (
            request.user == obj.author or request.user.is_staff
        ):
            return True

        return False
