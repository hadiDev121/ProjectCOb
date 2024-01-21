# myApp/urls.py
from django.urls import path
from .views import upload, convert

urlpatterns = [
    path('', upload, name='upload'),
    path('convert/<int:pdf_id>/', convert, name='convert'),
]
