from django.urls import path
from .views.CV import CVUploadView

urlpatterns = [
    path("", CVUploadView.as_view(), name="cv_upload"),
]
