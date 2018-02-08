from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login_index),
    url(r'^register$', views.register),
    url(r'^userlogin$', views.userlogin),
    url(r'^userlogout$', views.userlogout),
    url(r'^user/(?P<user_id>\d+)$', views.show),
    url(r'^user/$', views.show_error, ), # This route captures a user's click to profile page when not logged in and routes him to views.show_error which will see his missing session ID and return a flash error message.
    # url(r'^print_ses$', views.print_ses), # For testing login page
    
]