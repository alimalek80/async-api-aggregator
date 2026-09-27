from django.urls import path
from . import views

urlpatterns = [
    path('sync/', views.SyncBenchmarkView.as_view(), name='sync-benchmark'),
    path('async/', views.async_benchmark, name='async-benchmark'),
]