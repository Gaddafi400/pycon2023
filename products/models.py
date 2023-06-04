from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField

FEATURED = (
    (0, 'No'),
    (1, 'Everywhere'),
    (2, 'Category')
)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    location = models.CharField(max_length=10, unique=True)
    serial_number = models.CharField(max_length=40, unique=True)
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    featured = models.IntegerField(choices=FEATURED, default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


def _image_upload(instance, filename):
    return f'products/{instance.product.slug}/{filename}'


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to=_image_upload)
    cropping = ImageRatioField('image', '430x360')

    class Meta:
        ordering = ['order']
        unique_together = ('product', 'order')

    def __str__(self):
        return f'Image {self.order} for {self.product}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
