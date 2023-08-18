from rest_framework import permissions


class ChangeObjectIfAuthor(permissions.BasePermission):
    """
    Custom permission to allow only GET requests and authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated == obj.author
