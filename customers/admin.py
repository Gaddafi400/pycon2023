from django.contrib import admin
from django.db.models import Count, Sum
from django.utils import timezone
from .forms import CustomerForm
from .models import Customer, PurchaseItem, Purchase, PurchaseSummary


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
    form = CustomerForm
    list_display = ['admin_name', 'name']
    search_fields = ['name']
    save_on_top = True
    save_as = True


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem


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
    inlines = [PurchaseItemInline]

    fieldsets = (
        (None, {
            'fields': (
                ('customer', 'total', 'shipped'),
                'discount_code'
            )
        }),
        ('Date', {
            'classes': ('collapse',),
            'fields': ('placed_at', 'shipped_at')
        })
    )


@admin.register(PurchaseSummary)
class PurchaseSummaryAdmin(admin.ModelAdmin):
    date_hierarchy = 'purchase__placed_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
            # print('🚫', list(qs))
            # print('✳️', list(qs.values()))
            # print(response.context_data.items())
        except (AttributeError, KeyError):
            return response

        metrics = {'total': Sum('quantity'), 'total_sale': Sum('product__price')}
        response.context_data['summary'] = list(qs.values('product__name').annotate(**metrics).order_by('-quantity'))
        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))
        # print('response ✂️', response.context_data['summary_total'])
        return response
