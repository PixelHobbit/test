from django.urls import path
from . import views

# start with share
urlpatterns = [
    # http://localhost:8000/share/
    path('', views.share_list, name='share_list'),
    path('<int:share_pk>', views.share_detail, name="share_detail"),
    path('type/<int:share_type_pk>', views.shares_with_type, name="shares_with_type"),
    path('date/<int:year>/<int:month>', views.shares_with_date, name="shares_with_date"),
]
