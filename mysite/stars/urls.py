from django.urls import path
from . import views

urlpatterns = [
    path('', views.stars_list, name='stars_list'),
    path('<int:star_pk>', views.star_detail, name="star_detail"),
]
