from rest_framework import serializers

from .models import CustomUser, Ticket, TicketAttachment, TicketComment


class UserSerializer(serializers.ModelSerializer):
    """Basic user info shown in tickets"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "department",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class TicketAttachmentSerializer(serializers.ModelSerializer):
    """Handles file uploads"""

    class Meta:
        model = TicketAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["uploaded_at"]


class TicketCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = TicketComment
        fields = ["id", "author", "message", "is_internal", "created_at"]
        read_only_fields = ["author"]


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "category",
            "priority",
            "status",
            "created_by",
            "assigned_to",
            "created_at",
            "updated_at",
            "resolved_at",
            "attachments",
            "comments",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at", "resolved_at"]


class TicketCreateSerializer(serializers.ModelSerializer):
    """Used when creating a ticket (supports file uploads in one request)"""

    attachments = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "category", "priority", "attachments"]

    def create(self, validated_data):
        attachments = validated_data.pop("attachments", [])
        ticket = Ticket.objects.create(
            **validated_data, created_by=self.context["request"].user
        )

        for file in attachments:
            TicketAttachment.objects.create(ticket=ticket, file=file)

        return ticket


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    """Used by IT staff to update status and assign tickets"""

    class Meta:
        model = Ticket
        fields = ["status", "assigned_to"]


# ==================== END OF SERIALIZERS ====================
