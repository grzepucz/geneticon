"""ga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from geneticon import views
from django.contrib import admin
from django.urls import path
from geneticon.services import configuration

urlpatterns = [
    path('', views.home, name='home'),
    path('configuration', views.configuration, name='configuration'),
    path('life/<int:life_id>', views.life, name='life'),
    path('life/<int:life_id>/epoch/<int:epoch_number>', views.epoch_analyze, name='epoch_analyze'),
    path('life/<int:life_id>/metrics/epoch/<int:epoch_number>', views.epoch_metrics, name='epoch_metrics'),
    path('life/<int:life_id>/metrics', views.epoch_metrics_animate, name='epoch_metrics_animate'),
    path('life/<int:life_id>/epoch/<int:epoch_number>/clean', views.epoch_clean, name='epoch_clean'),
    path('preconfigure', views.preconfigure),
    path('life/<int:life_id>/clean', views.armageddon, name='life_clean')
]
