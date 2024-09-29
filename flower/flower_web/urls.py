from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.make_prediction, name='make_prediction'),  # Separate path for predictions
]
