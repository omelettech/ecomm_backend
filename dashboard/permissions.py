# dashboard/permissions.py
from rest_framework.permissions import BasePermission

# class IsArtistUser(BasePermission):
#     def has_permission(self, request, view):
#         return hasattr(request.user, 'profile') and request.user.profile.role == 'artist'

class IsArtistUser(BasePermission):
    def has_permission(self, request, view):
        return True
    # TODO: Change
