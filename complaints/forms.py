from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from complaints.models import (
    Complaint,
    Department,
    ComplaintCategory,
    ComplaintSubCategory,
    UserProfile
)


# =========================
# Complaint Form
# =========================

class ComplaintForm(forms.ModelForm):

    class Meta:

        model = Complaint

        fields = [

            'first_name',
            'last_name',

            'email',
            'phone',

            'title',
            'description',

            'category',
            'subcategory',
            'department',

            'location',
            'incident_date',
            'attachment',

            'priority',

            'is_anonymous',

            'role'

        ]

        widgets = {

            'role': forms.TextInput(
                attrs={
                    'readonly': True
                }
            )

        }

    def __init__(
        self,
        *args,
        **kwargs
    ):

        user = kwargs.pop(
            'user',
            None
        )

        super().__init__(
            *args,
            **kwargs
        )

        # =========================
        # QUERYSETS
        # =========================

        self.fields[
            'department'
        ].queryset = Department.objects.all()

        self.fields[
            'category'
        ].queryset = ComplaintCategory.objects.all()

        self.fields[
            'subcategory'
        ].queryset = ComplaintSubCategory.objects.all()

        # =========================
        # OPTIONAL FIELDS
        # =========================

        self.fields[
            'phone'
        ].required = False

        self.fields[
            'location'
        ].required = False

        self.fields[
            'incident_date'
        ].required = False

        self.fields[
            'attachment'
        ].required = False

        # =========================
        # ROLE FIELD
        # =========================

        self.fields[
            'role'
        ].disabled = True

        # =========================
        # USER AUTO FILL
        # =========================

        if user and user.is_authenticated:

            try:

                profile = (
                    UserProfile.objects
                    .get(user=user)
                )

                self.fields[
                    'first_name'
                ].initial = (
                    profile.first_name
                )

                self.fields[
                    'last_name'
                ].initial = (
                    profile.last_name
                )

                self.fields[
                    'email'
                ].initial = (
                    profile.email
                )

                self.fields[
                    'phone'
                ].initial = (
                    profile.mobile_number
                )

                # ROLE SHOW FIX
                self.fields[
                    'role'
                ].initial = (
                    profile.get_role_display()
                )

            except UserProfile.DoesNotExist:

                self.fields[
                    'first_name'
                ].initial = (
                    user.first_name
                )

                self.fields[
                    'last_name'
                ].initial = (
                    user.last_name
                )

                self.fields[
                    'email'
                ].initial = (
                    user.email
                )


# =========================
# Register Form
# =========================

PUBLIC_ROLE_CHOICES = [

    ('student', 'Student'),

    ('teacher', 'Teacher'),

    ('staff', 'Staff'),

]


class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=100
    )

    last_name = forms.CharField(
        max_length=100
    )

    email = forms.EmailField()

    role = forms.ChoiceField(
        choices=PUBLIC_ROLE_CHOICES
    )

    department = forms.CharField(
        max_length=100, required=False
    )

    mobile_number = forms.CharField(
        max_length=15
    )

    class Meta:

        model = User

        fields = [

            'first_name',

            'last_name',

            'username',

            'email',

            'role',

            'department',

            'mobile_number',

            'password1',

            'password2'

        ]


# =========================
# Complaint Assignment Form
# =========================

class ComplaintAssignmentForm(
    forms.ModelForm
):

    class Meta:

        model = Complaint

        fields = [
            'assigned_to',
        ]
