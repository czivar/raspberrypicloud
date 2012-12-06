from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',


    url(r'^$', 'cluster.views.home', name='home'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/profile/$', 'cluster.views.profile', name='profile'),
    url(r'^accounts/logout/$', 'cluster.views.logout_view', name='logout'),

    url(r'^node/pi(?P<nodeid>\d+)/$', 'cluster.views.node'),
    url(r'^node/$', 'cluster.views.nodes', name='nodes'),

    url(r'^services/$', 'cluster.views.services', name='services'),

    url(r'^vm/$', 'cluster.views.vm', name='vms'),
    url(r'^vm/start/$', 'cluster.views.vmstart', name='vmstart'),

    url(r'^templates/$', 'cluster.views.templates', name='templates'),
    url(r'^template/(?P<id>\d+)/$', 'cluster.views.template', name='template'),
    url(r'^template/delete/(?P<id>\d+)/$', 'cluster.views.template_delete', name='template_delete'),
    url(r'^template/add/$', 'cluster.views.templates', name='template_add'),    
    
	url(r'^vms/$', 'cluster.views.vms', name='vms'),
    url(r'^vm/(?P<id>\d+)/$', 'cluster.views.vm', name='vm'),
    url(r'^vm/delete/(?P<id>\d+)/$', 'cluster.views.vm_delete', name='vm_delete'),
    url(r'^vm/add/$', 'cluster.views.vms', name='vm_add'),    

)
