from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)
