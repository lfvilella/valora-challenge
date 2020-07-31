from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)


class Address(models.Model):
    class Meta:
        abstract = True

    STATE_CHOICES = (
        ('sp', 'SP'),
        ('pr', 'PR'),
        ('mg', 'MG'),
    )

    state = models.CharField(
        max_length=30, choices=STATE_CHOICES, null=True, blank=True
    )
    endereco = models.CharField(max_length=255, null=True, blank=True)
    neighborhood = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    complement = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    cep = models.CharField(max_length=12, null=True, blank=True)


class Advertiser(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    phone =
    company_link =


class Tool(BaseModel):
    name = models.Charfield(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)


class Order(BaseModel):
    item = models.ForeignKey(Tool, on_delete=models.CASCADE, null=False, blank=False)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=False)
    contact_information = # foreingkey de Anunciante
    status = models.BooleanField(default=True)
