from django.urls import path, include
from .views import(
    KalafexAdminRegisterView,
    ArtistRegisterView,
    CustomerRegisterView,
    AddressCreateView,
    ArtistUpdateDeleteView,
    CustomerUpdateDeleteView,
    AddressUpdateDeleteView,
    ParticularAddressView,
    AddressListView,
    ParticularArtistView,
    ArtistListView,
    CashOutRequestView,
    CashOutView,
    GrantCashOutView
)

urlpatterns = [
    path('kalafex_admin/', KalafexAdminRegisterView.as_view()),
    path('artist/', ArtistRegisterView.as_view()),
    path('customer/', CustomerRegisterView.as_view()),
    path('add_address/', AddressCreateView.as_view()),
    path('modify_artist/', ArtistUpdateDeleteView.as_view()),
    path('modify_customer/', CustomerUpdateDeleteView.as_view()),
    path('modify_address/<str:a_id>/', AddressUpdateDeleteView.as_view()),
    path('view_particular_address/<str:a_id>/', ParticularAddressView.as_view()),
    path('view_addresses/', AddressListView.as_view()),
    path('view_particular_artist/<str:custom_url>/', ParticularArtistView.as_view()),
    path('view_artists/', ArtistListView.as_view()),
    path('request/cashout/', CashOutRequestView.as_view()),
    path('view/cashout_requests/', CashOutView.as_view()),
    path('grant/cashout/', GrantCashOutView.as_view())
]
