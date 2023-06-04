from django.contrib import admin
from .models import Product, Image, Category
from image_cropping import ImageCroppingMixin


@admin.register(Image)
class ImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class ImageInline(ImageCroppingMixin, admin.StackedInline):
    model = Image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'price']
    fields = (
        ('name', 'slug'),
        'description',
        ('price', 'quantity'),
        ('featured',),
        ('serial_number', 'location'),
        'categories'
    )
    radio_fields = {'featured': admin.HORIZONTAL}
    filter_horizontal = ['categories']
    inlines = [ImageInline]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
