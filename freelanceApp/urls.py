from django.contrib import admin
from django.urls import path
from freelanceApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('development', views.development, name='development'),
    path('ai', views.ai, name='ai'),
    path('animation', views.animation, name='animation'),
    path('audio', views.audio, name='audio'),
    path('cuscare', views.cuscare, name='cuscare'),
    path('design', views.design, name='design'),
    path('marketing', views.marketing, name='marketing'),
    path('writing', views.writing, name='writing'),
    path('join', views.join, name='join'), 
    path('find_work', views.find_work, name='find_work'),
    path('project/<int:project_id>/apply/', views.apply_project, name='apply_project'),
    
    path('freelancer_dashboard', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('freelancer_profile_view', views.freelancer_profile_view , name='freelancer_profile_view'),
    path('freelance_edit_profile', views.freelance_edit_profile , name='freelance_edit_profile'),
    path('freelance_projects', views.freelance_projects , name='freelance_projects'),
    path('freelancer_bid', views.freelancer_bid , name='freelancer_bid'),
    path('freelancer_inbox', views.freelancer_inbox , name='freelancer_inbox'),
    path('freelancer_earnings', views.freelancer_earnings , name='freelancer_earnings'),
    path('freelancer_withdraw_funds', views.freelancer_withdraw_funds , name='freelancer_withdraw_funds'),
    path('freelancer_bank_details', views.freelancer_bank_details , name='freelancer_bank_details'),
    path('freelancer_logout', views.freelancer_logout , name='freelancer_logout'),
    path('freelancer_perform_logout', views.freelancer_perform_logout, name='freelancer_perform_logout'),
    
    path('client_dashboard', views.client_dashboard , name='client_dashboard'),
    path('client_view_profile', views.client_view_profile , name='client_view_profile'),
    path('client_edit_profile', views.client_edit_profile , name='client_edit_profile'),
    path('client_post_project', views.client_post_project , name='client_post_project'),
    path('client_manage_project', views.client_manage_project , name='client_manage_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('view_project/<int:project_id>/', views.view_project, name='view_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('client_project_bids', views.client_project_bids , name='client_project_bids'),
    # path('client/project/<int:project_id>/bids/', views.project_bids_view, name='client_project_bids'),
    path('client_inbox', views.client_inbox , name='client_inbox'),
    path('client_bank_details', views.client_bank_details , name='client_bank_details'),
    path('client_payments', views.client_payments , name='client_payments'),
    path('client_logout', views.client_logout , name='client_logout'),
    path('client_perform_logout', views.client_perform_logout, name='client_perform_logout'),

    path('sign_up', views.sign_up , name='sign_up'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)