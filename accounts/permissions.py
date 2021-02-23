from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class IsKalafexAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_kalafex_admin)

class IsArtist(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_artist)