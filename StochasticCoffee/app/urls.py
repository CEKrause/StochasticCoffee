from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$',views.login, name='login'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile$', views.profile, name='profile'),    
#    url(r'^login/profile.html$', views.Profile.as_view(), name='profile'),    

]