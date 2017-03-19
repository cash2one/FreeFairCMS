from rest_framework.permissions import BasePermission


class IsAdminEditor(BasePermission):
    """
    Allow access only to Editors with Admin role
    """
    def has_permission(self, request, view):
        try:
            return request.user and request.user.role == 'A'
        except AttributeError:
            return False
