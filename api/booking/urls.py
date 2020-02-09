import logging
from django.urls import path
from booking.views import ScreenView, ReserveView, SeatView

__author__ = "akhtar"


logger = logging.getLogger(__name__)


urlpatterns = [
    path('screens', ScreenView.as_view(), name="screens"),
    path('screens/<str:screen_name>/reserve', ReserveView.as_view(), name='screen_reserve'),
    path('screens/<str:screen_name>/seats', SeatView.as_view(), name='screen_seats'),
]
