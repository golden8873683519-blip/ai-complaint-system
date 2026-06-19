from django.core.mail import EmailMessage
from .models import Notification


ADMIN_EMAIL = "devender2643@gmail.com"


def send_event_email(event, complaint, recipients):
    subject_map = {
        "created": "🆕 New Complaint Registered",
        "assigned": "📌 Complaint Assigned Successfully",
        "status_pending": "⏳ Complaint Status: Pending",
        "status_progress": "⚙️ Complaint In Progress",
        "status_resolved": "✅ Complaint Resolved Successfully",
        "feedback_submitted": "⭐ New Complaint Feedback Received",
    }

    subject = subject_map.get(event, "📢 Complaint Update Notification")

    if event == "feedback_submitted":

        body = f"""
    Hello Admin / Department Head,

    ⭐ A new feedback has been submitted.

    ━━━━━━━━━━━━━━━━━━━━━━
    📌 Complaint ID : {complaint.complaint_id}
    📌 Title        : {complaint.title}
    📌 Category     : {complaint.category}
    📌 Status       : {complaint.status}
    ━━━━━━━━━━━━━━━━━━━━━━

    Please login and review the feedback.

    College Complaint Management System
    """

    else:

        body = f"""
    Hello,

    You are receiving this notification regarding a complaint update in the system.

    ━━━━━━━━━━━━━━━━━━━━━━
    📌 Complaint ID : {complaint.complaint_id}
    📌 Title        : {complaint.title}
    📌 Category     : {complaint.category}
    📌 Status       : {complaint.status}
    ━━━━━━━━━━━━━━━━━━━━━━

    Please log in to the system for more details.

    This is an automated email from College Complaint Management System.

    Regards,
    Admin Team
    """

    EmailMessage(
        subject=subject,
        body=body,
        from_email="College Complaint System <yourgmail@gmail.com>",
        to=recipients
    ).send(fail_silently=False)


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_student(user):
    return user.groups.filter(name="Student").exists()


def create_notification(users, title, message, notification_type="system"):

    if not isinstance(users, list):
        users = [users]

    for user in users:

        if user:
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                type=notification_type
            )
