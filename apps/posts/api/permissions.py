from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS - разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Редактирование разрешено - только автору
        return obj.author == request.user