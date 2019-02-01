from django.urls import path
from . import views

# start with view
urlpatterns = [
    # http://localhost:8000/view/
    path('', views.view_list, name='view_list'),
    path('<int:view_pk>', views.view_detail, name="view_detail"),
    path('type/<int:view_type_pk>', views.views_with_type, name="views_with_type"),
    path('date/<int:year>/<int:month>', views.views_with_date, name="views_with_date"),
]
