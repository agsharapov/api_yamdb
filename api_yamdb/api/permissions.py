from rest_framework import permissions

OBSERVER_METHODS = ['GET']


class Admin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in OBSERVER_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in OBSERVER_METHODS


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in permissions.SAFE_METHODS \
            or obj.author == request.user or (
                request.user.is_authenticated and (
                    user.is_admin or user.is_moderator))
