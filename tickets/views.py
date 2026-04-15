from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView  # ← This was missing!

from .models import Ticket, TicketAttachment, TicketComment
from .serializers import (
    TicketAttachmentSerializer,
    TicketCommentSerializer,
    TicketCreateSerializer,
    TicketSerializer,
    TicketStatusUpdateSerializer,
    UserSerializer,
)


class IsEmployeeOrIT(permissions.BasePermission):
    """Custom permission: Employees can view, IT staff can modify"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        # Only IT staff or Admin can change status, assign, etc.
        return request.user.role in ["it_staff", "admin"]


class TicketViewSet(viewsets.ModelViewSet):
    """
    Main API for tickets.
    Employees can create & view their tickets.
    IT Staff can manage all tickets.
    """

    def get_queryset(self):
        queryset = Ticket.objects.all().order_by("-created_at")
        user = self.request.user

        # Filter based on query param ?filter=
        filter_type = self.request.query_params.get("filter")

        if filter_type == "my_tickets":
            queryset = queryset.filter(created_by=user)
        elif filter_type == "assigned_to_me":
            queryset = queryset.filter(assigned_to=user)
        elif filter_type == "open":
            queryset = queryset.filter(status__in=["open", "assigned"])
        # IT staff & admin see everything by default

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return TicketCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return TicketStatusUpdateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save()  # Creation logic is handled in TicketCreateSerializer

    # ===================== FILE UPLOAD =====================
    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser, FormParser])
    def upload_attachment(self, request, pk=None):
        """Upload extra files to an existing ticket"""
        ticket = self.get_object()
        files = request.FILES.getlist("file")

        if not files:
            return Response(
                {"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        attachments = []
        for file in files:
            attachment = TicketAttachment.objects.create(ticket=ticket, file=file)
            attachments.append(TicketAttachmentSerializer(attachment).data)

        return Response(attachments, status=status.HTTP_201_CREATED)

    # ===================== ADD COMMENT =====================
    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(ticket=ticket, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ===================== ASSIGN TICKET =====================
    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        if request.user.role not in ["it_staff", "admin"]:
            return Response(
                {"detail": "Only IT staff can assign tickets"},
                status=status.HTTP_403_FORBIDDEN,
            )

        ticket = self.get_object()
        assigned_to_id = request.data.get("assigned_to")

        if assigned_to_id:
            ticket.assigned_to_id = assigned_to_id
            if ticket.status == "open":
                ticket.status = "assigned"
            ticket.save()
            from .tasks import send_ticket_notification

            send_ticket_notification.delay(ticket.id, "Assigned")
            return Response(TicketSerializer(ticket).data)

        return Response(
            {"detail": "assigned_to field is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ===================== VIDEO CALL =====================
    @action(detail=True, methods=["get"])
    def video_call(self, request, pk=None):
        """Returns Jitsi Meet URL for this ticket"""
        ticket = self.get_object()
        url = ticket.get_jitsi_url()
        return Response({"video_url": url, "room_name": ticket.jitsi_room})


class CurrentUserView(APIView):
    """Returns info about the currently logged-in user"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
