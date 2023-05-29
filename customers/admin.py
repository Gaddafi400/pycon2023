from django.contrib import admin
from django.db.models import Count
from django.utils import timezone

from .models import Customer, PurchaseItem, Purchase


# custom filtering
class BigOrderFilter(admin.SimpleListFilter):
    title = 'big order'
    parameter_name = 'big_order'

    def lookups(self, request, model_admin):
        return ('1', 'True'), ('0', 'False')

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.annotate(Count('items')).filter(items__count__gte=2)
        return queryset


# action
def ship(model_admin, request, queryset):
    queryset.update(shipped=True, shipped_at=timezone.now())


ship.short_description = 'Mark purchases as shipped now'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['admin_name', 'name']


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    actions = [ship]
    list_display = ['customer', 'placed_at', 'shipped_at', 'shipped', 'total']
    list_editable = ['shipped']
    list_per_page = 10
    list_filter = ['shipped', 'placed_at', 'shipped_at', BigOrderFilter]
    ordering = ['placed_at']
    search_fields = ['customer__name', 'items__name']
    search_help_text = 'Search by customer name of item name'
