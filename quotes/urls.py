from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name='root'),
    path("page/<int:page>/", views.main, name="root_paginate"),
]
