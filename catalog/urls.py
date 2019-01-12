from django.urls import include
from django.urls import path

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]