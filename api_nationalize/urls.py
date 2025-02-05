from django.urls import path

from .views import NameAPIView, index

urlpatterns = [
    path('', index, name='index'),
    path("names/", NameAPIView.as_view(), name="names"),
]
