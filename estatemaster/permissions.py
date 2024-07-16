from rest_framework import permissions


class IsAccountConfirmed(permissions.BasePermission):
    message = "Your account must be confirmed to perform this action."

    def has_permission(self, request, view):
        # Проверяем, активирован ли пользователь и подтверждён ли его аккаунт
        return request.user.is_active or getattr(request.user, 'is_confirm', False)