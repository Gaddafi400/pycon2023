from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('category/<slug:category>/', views.ByCategory.as_view(), name='category'),
    path('view/<slug:slug>/', views.Detail.as_view(), name='detail'),
    path('', views.AllProducts.as_view(), name='list'),
]

# from django.conf.urls import url
#
# from . import views
#
# urlpatterns = [
#     url(r'^category/(?P<category>[-\w]+)/$', views.ByCategory.as_view(), name='category'),
#     url(r'^view/(?P<slug>[-\w]+)/$', views.Detail.as_view(), name='detail'),
#     url(r'^$', views.AllProducts.as_view(), name='list'),
# ]


