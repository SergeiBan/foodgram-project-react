from rest_framework import permissions


class AuthorOrAuthenticatedElseReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            return request.user.is_authenticated and request.user == obj.author
        if request.method == 'GET':
            return True

        return False


class AdminOnlyUnsafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'):
            return True

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'):
            return True
