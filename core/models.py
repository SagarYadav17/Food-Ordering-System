from django.db import models

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


class Tag(TimestampedModel):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    rank = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["rank"]

    def __str__(self):
        return self.name


class MenuItem(TimestampedModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="menu_items", blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name="menu_items", limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="menu_items", limit_choices_to={"is_active": True})
    rank = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category__rank", "rank"]

    def __str__(self):
        return f"{self.name} - {self.category} - {self.is_active}"

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.is_active = False

        super().save(*args, **kwargs)


class Order(TimestampedModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("ready", "Ready"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    table_number = models.IntegerField()
    status = models.CharField(max_length=255, default="pending", choices=STATUS_CHOICES)

    def __str__(self):
        return str(self.table_number)


class OrderedItem(TimestampedModel):
    order = models.ForeignKey(Order, related_name="ordered_items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name="quantities", limit_choices_to={"is_active": True}, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.menu_item} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)


class Payment(TimestampedModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.order} - {self.price}"

    def save(self, *args, **kwargs):
        self.price = OrderedItem.objects.filter(order=self.order).aggregate(models.Sum("price"))["price__sum"]
        super().save(*args, **kwargs)
