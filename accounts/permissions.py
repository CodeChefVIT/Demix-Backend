from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class IsDemixAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_demix_admin)

class IsArtist(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_artist)