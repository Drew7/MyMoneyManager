"""mymoney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from mymoneymanager import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    #url(r'^$', views.DocumentListView.as_view(), name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    url(r'^documents/$', views.documents_list, name='documents'),
    url(r'^documents/income$', views.income_list, name='documents_income'),
    url(r'^documents/expence$', views.expence_list, name='documents_expence'),
    
    url(r'^documents/create/$', views.document_create, name='document_create'),
    url(r'^documents/(?P<pk>\d+)/update/$',
        views.document_update, name='document_update'),
    url(r'^documents/(?P<pk>\d+)/delete/$',
        views.document_delete, name='document_delete'),

    url(r'^currencies/$', views.currencies_list, name='currencies'),
    url(r'^countries/$', views.countries_list, name='countries'),
    url(r'^banks/$', views.banks_list, name='banks'),
    url(r'^wallets/$', views.wallets_list, name='wallets'),
    url(r'^counterparties/$', views.counterparties_list, name='counterparties'),
    url(r'^income_items/$', views.income_items_list, name='income_items'),
    url(r'^expence_items/$', views.expence_items_list, name='expence_items'),
    url(r'^exchange_rates/$', views.exchange_rates_list, name='exchange_rates'),
    
    url(r'^documents/(?P<pk>\d+)/$', views.documents, name='document'),
    url(r'^documents/(?P<pk>\d+)/edit/$',
        views.DocumentUpdateView.as_view(), name='edit_document'),
    url(r'^documents/(?P<pk>\d+)/new/$', views.new_document, name='new_document'),
    url(r'^admin/', admin.site.urls),
]
