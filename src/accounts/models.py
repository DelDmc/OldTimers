from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=35, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=156, blank=True)
    last_name = models.CharField(_("last name"), max_length=156, blank=True)
    birthdate = models.DateField(_("birthday"), null=True, blank=True)
    country = CountryField(blank=True, null=True)
    city = models.CharField(_("city"), max_length=64, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )

    photo = models.ImageField(upload_to="users_photo/", null=True, blank=True)

    objects = CustomerManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_owner(self):
        from oldtimers.models import Vehicle

        vehicles = Vehicle.objects.filter(owner_id=self.id)
        if vehicles:
            return True
        else:
            return False

    def is_retailer(self):
        from oldtimers.models import Vehicle

        vehicles = Vehicle.objects.filter(retailer__user_id=self.id)
        if vehicles:
            return True
        else:
            return False
