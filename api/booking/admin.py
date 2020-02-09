from django.contrib import admin

from booking.models import Row, Screen, Reserve


class RowAdmin(admin.ModelAdmin):
    list_per_page = 500
    ordering = ['id']
    list_display = ["id", "name", "no_of_seats", ]


class ScreenAdmin(admin.ModelAdmin):
    list_per_page = 500
    ordering = ['id']
    list_display = ["id", "name", ]


class ReserveAdmin(admin.ModelAdmin):
    list_per_page = 500
    ordering = ['id']
    list_display = ["id", "screen", "row", "seats_reserved", ]


admin.site.register(Row, RowAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(Reserve, ReserveAdmin)
