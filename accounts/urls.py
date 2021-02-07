from django.urls import path, include
from .views import(
    KalafexAdminRegisterView,
    ArtistRegisterView,
    CustomerRegisterView
)

urlpatterns = [
    path('kalafex_admin/', KalafexAdminRegisterView.as_view()),
    path('artist/', ArtistRegisterView.as_view()),
    path('customer/', CustomerRegisterView.as_view()),
]
