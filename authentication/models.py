from django.db import models
from core.models import TimestampedModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, fullname: str = None, phonenumber: int = None, password=None, email=None, user_type=None):
        """Create and return a `User` with an email, phone_number and password."""
        if not (fullname and phonenumber and password):
            raise TypeError("User must have a fullname, phonenumber and password.")

        user = self.model(phonenumber=phonenumber, fullname=fullname)
        user.set_password(password)

        if email:
            user.email = self.normalize_email(email)

        if user_type:
            user.user_type = user_type

        user.save()

        return user

    def create_superuser(self, fullname, phonenumber, password, email=None, user_type=None):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """

        user = self.create_user(fullname, phonenumber, password, email, user_type)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    USER_TYPES = (
        ("Customer", "Customer"),
        ("Merchant", "Merchant"),
    )
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    email = models.EmailField(max_length=128, unique=True, blank=True, null=True)
    phonenumber = models.PositiveIntegerField(db_index=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot log into the Django admin site.
    # For most users, this flag will always be false.
    is_staff = models.BooleanField(default=False)

    # More fields required by Django when specifying a custom user model.
    fullname = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50, default="Customer", choices=USER_TYPES)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = ["phonenumber", "fullname"]

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.username
