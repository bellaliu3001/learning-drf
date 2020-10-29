from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("api/test/", views.Test.as_view()),
    path("admin/", admin.site.urls),
]
