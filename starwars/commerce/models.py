# import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True

# id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)


class Address(models.Model):
    STATE_CHOICES = (
        ("AC", "AC"),
        ("AL", "AL"),
        ("AP", "AP"),
        ("AM", "AM"),
        ("BA", "BA"),
        ("CE", "CE"),
        ("DF", "DF"),
        ("ES", "ES"),
        ("GO", "GO"),
        ("MA", "MA"),
        ("MT", "MT"),
        ("MS", "MS"),
        ("MG", "MG"),
        ("PA", "PA"),
        ("PB", "PB"),
        ("PR", "PR"),
        ("PE", "PE"),
        ("PI", "PI"),
        ("RJ", "RJ"),
        ("RN", "RN"),
        ("RS", "RS"),
        ("RO", "RO"),
        ("RR", "RR"),
        ("SC", "SC"),
        ("SP", "SP"),
        ("SE", "SE"),
        ("TO", "TO"),
    )

    state = models.CharField(
        max_length=2, choices=STATE_CHOICES, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    neighborhood = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=25, null=True, blank=True)
    complement = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    cep = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return f"{self.city}/{self.state} - CEP: {self.cep}"


class Advertiser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f"{self.user} - {self.phone}"


class Item(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class Order(BaseModel):
    STATUS_OPEN = "open"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_FINISHED, "Finished"),
    )

    advertiser = models.ForeignKey(
        Advertiser, on_delete=models.CASCADE, null=False, blank=False
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=False, blank=False
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=False, blank=False
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=False,
        blank=False,
        default=STATUS_OPEN,
    )

    def __str__(self):
        return f"{self.item} - {self.status}"
