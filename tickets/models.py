from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom User model for our IT Support system.
    """

    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("it_staff", "IT Staff"),
        ("admin", "Administrator"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Ticket(models.Model):
    """
    Main Ticket model for the IT Support System.
    """

    STATUS_CHOICES = [
        ("open", "Open"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("pending_onsite", "Pending On-site Visit"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    CATEGORY_CHOICES = [
        ("hardware", "Hardware"),
        ("software", "Software"),
        ("network", "Network"),
        ("email", "Email & Collaboration"),
        ("access", "Access Rights"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tickets_created"
    )
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets_assigned",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # === NEW: Video Call Support ===
    jitsi_room = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]  # Newest tickets first

    def __str__(self):
        return f"Ticket #{self.id} - {self.title[:50]}"

    def get_jitsi_url(self):
        """Generate or return Jitsi Meet link for this ticket"""
        if not self.jitsi_room:
            # Auto-generate a unique room name
            self.jitsi_room = (
                f"ITSupport-{self.id}-{self.created_at.strftime('%Y%m%d%H%M')}"
            )
            self.save(update_fields=["jitsi_room"])
        return f"https://meet.jit.si/{self.jitsi_room}"


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="tickets/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Ticket #{self.ticket.id}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on Ticket #{self.ticket.id}"
