# main/urls.py
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^login/$', views.LoginPageView.as_view()),
    url(r'^signup/$', views.SignupPageView.as_view()),
    url(r'^profile/$', views.ProfilePageView.as_view()),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
]