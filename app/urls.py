from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'app.views.filechoosing', name='filechoosing'),
    url(r'^datachoosing$', 'app.views.datachoosing', name='datachoosing'),
    url(r'^result$', 'app.views.result', name='result'),
]
