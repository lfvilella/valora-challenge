from django.contrib import admin

from . import models


class AdvertiserInline(admin.StackedInline):
    model = models.Advertiser
    max_num = 1


class AddressInline(admin.StackedInline):
    model = models.Address
    max_num = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [AdvertiserInline, AddressInline]


admin.site.register(models.Order, OrderAdmin)


class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ["phone"]


admin.site.register(models.Advertiser, AdvertiserAdmin)


class ToolAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(models.Tool, ToolAdmin)
