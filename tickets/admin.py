from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Ticket, TicketAttachment, TicketComment


class CustomUserAdmin(UserAdmin):
    """Customize how users appear in Django Admin"""

    model = CustomUser
    list_display = ("username", "email", "role", "department", "is_staff")
    list_filter = ("role", "department", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role", "department")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_by",
        "assigned_to",
        "status",
        "priority",
        "created_at",
    )
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at", "resolved_at")


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "file", "uploaded_at")


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "is_internal", "created_at")
