from django.contrib import admin
from django.utils.html import format_html

from . import models


class AdvertiserInline(admin.StackedInline):
    model = models.Advertiser
    max_num = 1


class AddressInline(admin.StackedInline):
    model = models.Address
    max_num = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["item", "order_status"]
    inlines = [AdvertiserInline, AddressInline]

    def order_status(self, order):
        if order.status == "finished":
            _html = (
                '<svg xmlns="http://www.w3.org/2000/svg" width="24" '
                'height="24" viewBox="0 0 24 24"><path fill="none" d="M0 '
                '0h24v24H0V0zm0 0h24v24H0V0z"/><path d="M16.59 7.58L10 '
                "14.17l-3.59-3.58L5 12l5 5 8-8zM12 2C6.48 2 2 6.48 2 "
                "12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 "
                '0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/></svg>'
            )
            return format_html(_html)

        _html = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" '
            'height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" '
            'fill="none"/><path d="M14.59 8L12 10.59 9.41 8 8 9.41 10.59 12 '
            "8 14.59 9.41 16 12 13.41 14.59 16 16 14.59 13.41 12 16 "
            "9.41 14.59 8zM12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 "
            "10-10S17.53 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 "
            '8 8-3.59 8-8 8z"/></svg>'
        )
        return format_html(_html)


@admin.register(models.Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ["phone"]


@admin.register(models.Tool)
class ToolAdmin(admin.ModelAdmin):
    search_fields = ["name"]
