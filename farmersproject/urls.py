"""
URL configuration for farmersproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from farmerapp import views as farmerviews
from govtapp import views as govtviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',farmerviews.index,name="index"),
    path('about/',farmerviews.about,name="about"),
    path('admin-login/',farmerviews.adminlogin,name="adminlogin"),
    path('farmer-login/',farmerviews.farmerlogin,name="farmerlogin"),
    path('farmer-register/',farmerviews.farmerregister,name="farmerregister"),
    path('govt-officer-register/',farmerviews.admin_login,name="govtlogin"),
    path('agriculture-experts/',farmerviews.expertlogin,name="expertlogin"),
    path('contact/',farmerviews.contact,name="contact"),



    path('farmer-dashboard/',farmerviews.dashboard,name="dashboard"),
    path('crop-disease-detection/',farmerviews.cropdisease,name="cropdisease"),
    path('profile/',farmerviews.profile,name="profile"),

    path('farmer-feedback/',farmerviews.feedback,name="farmer_feedback"),
    path('logout/',farmerviews.user_logout,name="log_out"),
    path('chatbot/',farmerviews.chatbot,name="chatbot"),









    path('govt-officer',govtviews.index,name="govt_dashboard"),
    path('all-users/', govtviews.all_users, name='all_users'),
    path('pending-users/', govtviews.pending_users, name='pending_users'),
    path('feedback/', govtviews.feedback, name='feedback'),
    path('sentiment/', govtviews.sentiment, name='sentiment'),
    path('govt-graph/', govtviews.graph, name='govt_graph'),

    path('accept-user/<int:user_id>/', govtviews.accept_user, name='accept_user'),
    path('reject-user/<int:user_id>/', govtviews.reject_user, name='reject_user'),
    path('delete-user/<int:user_id>/', govtviews.delete_user, name='delete_user'),

















    




    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
