from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CurrentUserView, TicketViewSet

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/me/", CurrentUserView.as_view(), name="current-user"),
    # Example: POST to /api/tickets/1/add_comment/
    # Example: POST to /api/tickets/1/assign/
]
