
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('login.html', views.login, name='login'),
    path('documents.html', views.documents, name='documents'),
    path('upload.html',views.upload, name='upload'),
    path('contact.html', views.contact, name='contact'),
    path('signup.html', views.signup, name='signup'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('thanqu.html', views.thanqu, name='thanqu'),
    path('download.html', views.download, name='download'),
    path('dashboard.html', views.dashboard, name='dashboard'),
    path('register_admin.html', views.register_admin, name='register_admin'),
    path('prvdown.html', views.prvdown, name='prvdown'),
    path('admin_view.html',views.admin_view, name='admin_view'),
  
    
]
