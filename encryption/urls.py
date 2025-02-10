from django.urls import path
from .views import upload_file, index

urlpatterns = [
    path('', index, name='index'),  # Serves the homepage
    path('upload/', upload_file, name='upload_file'),  # Handles file uploads and processing
]

