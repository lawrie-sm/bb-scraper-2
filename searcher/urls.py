from django.conf.urls import url
from searcher import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^search/$', views.SPSearchResults.as_view(), name='search')
]