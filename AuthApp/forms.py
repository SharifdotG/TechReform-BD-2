"""
Django forms for user authentication and profile management.

This module contains Django form classes that handle user registration, authentication,
profile management, and password reset functionality. The forms provide validation,
custom field handling, and integration with the UserProfile model.

Forms included:
    - CustomUserCreationForm: Enhanced user registration with profile fields
    - CustomAuthenticationForm: Login form with remember me functionality
    - UserProfileForm: Profile editing and management
    - PasswordChangeRequestForm: Request password reset via email
    - PasswordResetForm: Set new password with confirmation validation

All forms include proper validation, error handling, and follow Django best practices
for security and user experience.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with extended profile fields.

    This form extends Django's built-in UserCreationForm to include additional
    fields required for user registration such as email, names, phone, and role.
    It automatically creates a UserProfile instance when a user is registered.

    Additional Fields:
        email (EmailField): User's email address (required)
        first_name (CharField): User's first name (required, max 30 chars)
        last_name (CharField): User's last name (required, max 30 chars)
        phone (CharField): User's phone number (required, max 20 chars)
        role (ChoiceField): User's role in the system (defaults to 'user')

    Methods:
        save(commit=True): Saves the user and creates associated UserProfile

    Example:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, initial="user", required=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        """
        Save the user instance and create associated UserProfile.

        This method extends the parent save() to include additional field
        processing and UserProfile creation with phone and role information.

        Args:
            commit (bool): Whether to save to database immediately. Defaults to True.

        Returns:
            User: The created user instance with associated profile.

        Note:
            If commit=False, the UserProfile will not be created until the
            user is saved to the database.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            # Create or update user profile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.phone = self.cleaned_data["phone"]
            user_profile.role = self.cleaned_data["role"]
            user_profile.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with remember me functionality.

    This form extends Django's built-in AuthenticationForm to include a
    'remember me' checkbox that allows users to stay logged in for extended
    periods. The form maintains all standard authentication validation while
    adding session persistence options.

    Additional Fields:
        remember_me (BooleanField): Optional checkbox for extended session
                                  (defaults to False, not required)

    Usage:
        The remember_me field can be used in views to set session expiry:

        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser close
    """

    remember_me = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ("username", "password", "remember_me")


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.

    This ModelForm allows users to update their profile information including
    personal details from the User model (first name, last name, email) and
    profile-specific fields from the UserProfile model (phone, address, image).

    Fields:
        first_name (CharField): User's first name (required, max 30 chars)
        last_name (CharField): User's last name (required, max 30 chars)
        email (EmailField): User's email address (required)
        phone (CharField): Phone number from UserProfile
        address (TextField): Address from UserProfile
        profile_image (ImageField): Profile picture from UserProfile

    Methods:
        __init__: Initializes form with current user data pre-populated

    Example:
        form = UserProfileForm(request.POST, request.FILES,
                             instance=user.profile, user=user)
        if form.is_valid():
            form.save()
    """

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ("phone", "address", "profile_image")

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with user data pre-populated.

        This method extracts the user instance from kwargs and pre-populates
        the User model fields (first_name, last_name, email) with current values.

        Args:
            user (User, optional): User instance to pre-populate fields from
            *args: Variable length argument list passed to parent
            **kwargs: Arbitrary keyword arguments, 'user' is extracted if present
        """
        user = kwargs.pop("user", None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email


class PasswordChangeRequestForm(forms.Form):
    """
    Form for requesting a password reset via email.

    This simple form collects the user's email address to initiate the password
    reset process. The email is used to send a password reset link to the user.

    Fields:
        email (EmailField): Email address to send reset link to (required)

    Usage:
        This form is typically used in conjunction with Django's password reset
        views or custom password reset functionality.

    Example:
        form = PasswordChangeRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Send password reset email logic here
    """

    email = forms.EmailField(required=True)


class PasswordResetForm(forms.Form):
    """
    Form for setting a new password with confirmation.

    This form allows users to set a new password by requiring them to enter
    it twice for confirmation. It includes validation to ensure both password
    fields match before allowing the form to be considered valid.

    Fields:
        password1 (CharField): New password field with password widget
        password2 (CharField): Password confirmation field with password widget

    Methods:
        clean(): Custom validation to ensure passwords match

    Validation:
        - Both password fields must be filled
        - Both passwords must match exactly
        - Raises ValidationError if passwords don't match

    Example:
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()
    """

    password1 = forms.CharField(widget=forms.PasswordInput(), label="New Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm New Password"
    )

    def clean(self):
        """
        Validate that both password fields match.

        This method performs cross-field validation to ensure the user has
        entered the same password in both fields. If they don't match, a
        ValidationError is raised.

        Returns:
            dict: Cleaned data if validation passes

        Raises:
            ValidationError: If passwords don't match or are missing

        Note:
            This method calls the parent clean() method first to ensure
            individual field validation has completed successfully.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data
