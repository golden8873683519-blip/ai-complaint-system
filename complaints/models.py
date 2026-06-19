import random
import string
import re
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# =========================
# USER PROFILE
# =========================

ROLE_CHOICES = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('staff', 'Staff'),
    ('department_head', 'Department Head'),
]


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, blank=True, default="")
    last_name = models.CharField(max_length=50, blank=True, default="")

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    department = models.CharField(max_length=100)

    mobile_number = models.CharField(max_length=15, unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    is_department_head = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================
# EMAIL OTP
# =========================

class EmailOTP(models.Model):

    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def can_resend(self):
        return timezone.now() > self.created_at + timedelta(seconds=60)

    def __str__(self):
        return self.email


# =========================
# DEPARTMENT
# =========================

class Department(models.Model):

    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True)

    head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # validate department head role
        if self.head:
            try:
                profile = self.head.userprofile
                if profile.role != "department_head":
                    raise ValueError("User must be Department Head role")
            except:
                pass

        if not self.code:
            self.code = self.generate_code()

        super().save(*args, **kwargs)

    def generate_code(self):
        words = re.sub(r'[^a-zA-Z ]', '', self.name).upper().split()

        if len(words) == 1:
            base = words[0][:3]
        else:
            base = ''.join([w[0] for w in words])[:4]

        code = base
        counter = 1

        while Department.objects.filter(code=code).exists():
            code = f"{base}{counter}"
            counter += 1

        return code

    def __str__(self):
        return self.name


# =========================
# DEPARTMENT HEAD (KEEPED AS YOU WANT)
# =========================

class DepartmentHead(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, blank=True, default="")

    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =========================
# CATEGORY
# =========================

class ComplaintCategory(models.Model):

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# =========================
# SUBCATEGORY
# =========================

class ComplaintSubCategory(models.Model):

    category = models.ForeignKey(ComplaintCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# =========================
# COMPLAINT
# =========================
class Complaint(models.Model):

    complaint_id = models.CharField(
        max_length=20, unique=True, blank=True, null=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('EMERGENCY', 'Emergency'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    roll_number = models.CharField(max_length=50, blank=True, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField()

    category = models.ForeignKey('ComplaintCategory', on_delete=models.CASCADE)

    subcategory = models.ForeignKey(
        'ComplaintSubCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    location = models.CharField(max_length=255, blank=True, null=True)

    incident_date = models.DateField(null=True, blank=True)

    attachment = models.FileField(
        upload_to='complaints/', null=True, blank=True)

    is_anonymous = models.BooleanField(default=False)

    role = models.CharField(max_length=50, default="Student")

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Low'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_complaints"
    )

    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assigned_at = models.DateTimeField(blank=True, null=True)
    processing_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    # ⭐ FEEDBACK SUPPORT (IMPORTANT ADDITION)
    @property
    def has_feedback(self):
        return hasattr(self, 'complaintfeedback')

    @property
    def feedback(self):
        return getattr(self, 'complaintfeedback', None)

    # =========================
    # AI TITLE GENERATOR
    # =========================
    def generate_ai_title(self):

        if not self.description:
            return "General Complaint"

        text = self.description.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = text.split()

        STOPWORDS = {
            "is", "are", "was", "were", "the", "a", "an", "and", "or", "in", "on", "at", "to",
            "since", "from", "of", "for", "with", "by", "not", "no", "be", "has", "have", "had",
            "this", "that", "it", "there", "here", "very", "isnt", "dont", "does", "did"
        }

        filtered = [w for w in words if w not in STOPWORDS]

        if len(filtered) < 4:
            return " ".join(words[:7]).title()

        issue_words = {
            "broken", "damage", "leak", "leaking", "not", "working",
            "failure", "fault", "issue", "problem", "damaged", "stopped", "missing"
        }

        location_words = {
            "hostel", "room", "bathroom", "classroom", "campus", "lab", "mess"
        }

        issue_keywords = []
        place_keywords = []

        for w in filtered:
            if w in location_words:
                place_keywords.append(w)
            elif w in issue_words:
                issue_keywords.append(w)

        subject = filtered[0] if filtered else "Issue"

        title_parts = [subject]

        title_parts.append("issue" if issue_keywords else "problem")

        if place_keywords:
            title_parts.append("in " + place_keywords[0])

        return " ".join(title_parts).capitalize()

    # =========================
    # SAVE OVERRIDE
    # =========================
    def save(self, *args, **kwargs):

        if not self.title:
            self.title = self.generate_ai_title()

        if not self.complaint_id and self.department:
            unique = str(uuid.uuid4())[:6].upper()
            self.complaint_id = f"CMP-{self.department.code}-{unique}"

        old_status = None

        if self.pk:
            old_status = Complaint.objects.filter(
                pk=self.pk).values_list('status', flat=True).first()

        if self.assigned_to and not self.assigned_at:
            self.assigned_at = timezone.now()

        if self.status == "In Progress" and old_status != "In Progress":
            self.processing_at = timezone.now()

        if self.status == "Resolved" and old_status != "Resolved":
            self.resolved_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_id} - {self.title or 'No Title'}"


# =========================
# NOTIFICATION
# =========================

class Notification(models.Model):

    TYPE_CHOICES = [
        ("email", "Email"),
        ("system", "System"),
        ("status", "Status Update"),
        ("assignment", "Assignment"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, default="Notification")
    message = models.TextField()

    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="system")

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class ComplaintFeedback(models.Model):
    complaint = models.OneToOneField(
        Complaint,
        on_delete=models.CASCADE,
        related_name="feedback"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(default=5)

    resolution_speed = models.CharField(
        max_length=50,
        blank=True
    )

    satisfaction = models.CharField(
        max_length=50,
        blank=True
    )

    comment = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.complaint.complaint_id} - {self.rating}⭐"
