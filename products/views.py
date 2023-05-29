from django.shortcuts import get_object_or_404
from django.views import generic

from . import models

import logging

db_logger = logging.getLogger('db')


class AllProducts(generic.ListView):
    model = models.Product


class ByCategory(generic.ListView):
    template_name = 'products/product_list.html'

    db_logger.info('info message', extra={'user': 'Qaddafi', 'custom_category': 'B'})
    db_logger.warning('warning message', extra={'user': 'Qaddafi', 'custom_category': 'B'})

    try:
        1 / 0
    except Exception as e:
        db_logger.exception(e, extra={'user': 'Qaddafi💥', 'custom_category': 'B'})

    def get_queryset(self):
        category = get_object_or_404(models.Category, name__iexact=self.kwargs.get('category'))
        return category.product_set.all()


class Detail(generic.DetailView):
    model = models.Product
