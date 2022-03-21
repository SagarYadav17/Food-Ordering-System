from django.db import models
from authentication.models import User

# Create your models here.


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["-created_at", "-updated_at"]


class Region(TimestampedModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Country(TimestampedModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="countries")
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=10)
    iso2 = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class State(TimestampedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.country.name}"


class City(TimestampedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.state.name}"


class Address(TimestampedModel):
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="addresses")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="addresses")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="addresses")

    # Fields
    title = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    # Google Maps API
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.phonenumber}"
