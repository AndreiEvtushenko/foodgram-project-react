from rest_framework import permissions


class ChangeObjectIfAuthorOrAdmin(permissions.BasePermission):
    """
    Пользовательский класс разрешений:
    - GET, HEAD, OPTIONS запросы разрешены для всех.
    - POST, PUT, PATCH, DELETE запросы разрешены только для аутентифицированных пользователей
      и авторов объектов.
    - Для администраторов разрешены все действия.
    """

    def has_permission(self, request, view):
        # Разрешаем GET, HEAD и OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем POST, PUT, PATCH и DELETE запросы только для аутентифицированных пользователей
        if request.user and request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD и OPTIONS запросы для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем PUT, PATCH и DELETE запросы только для авторов объектов и администраторов
        if request.user and (request.user == obj.author or request.user.is_staff):
            return True

        return False
