from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'app.views.welcome', name='home'),
    url(r'^filechoosing$', 'app.views.filechoosing', name='filechoosing'),
    url(r'^datachoosing$', 'app.views.datachoosing', name='datachoosing'),
    url(r'^result$', 'app.views.result', name='result'),
    #url(r'^admin/', include(admin.site.urls)),
]
