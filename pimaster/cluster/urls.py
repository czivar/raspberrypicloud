from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',


    url(r'^$', 'cluster.views.home', name='home'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/profile/$', 'cluster.views.profile', name='profile'),
    url(r'^accounts/logout/$', 'cluster.views.logout_view', name='logout'),

    url(r'^node/(?P<nodename>\w+)/$', 'cluster.views.node', name='node'),
    url(r'^node/$', 'cluster.views.nodes', name='nodes'),

    url(r'^templates/$', 'cluster.views.templates', name='templates'),
    url(r'^template/(?P<id>\d+)/$', 'cluster.views.template', name='template'),
    url(r'^template/delete/(?P<id>\d+)/$', 'cluster.views.template_delete', name='template_delete'),
    url(r'^template/add/$', 'cluster.views.templates', name='template_add'),    
	
    url(r'^users/$', 'cluster.views.users', name='users'),
    url(r'^user/delete/(?P<id>\d+)/$', 'cluster.views.user_delete', name='user_delete'),
    url(r'^user/add/$', 'cluster.views.users', name='user_add'),    
	    
	url(r'^vms/$', 'cluster.views.vms', name='vms'),
    url(r'^vm/delete/(?P<id>\d+)/$', 'cluster.views.vm_delete', name='vm_delete'),
    url(r'^vm/start/(?P<id>\d+)/$', 'cluster.views.vm_start', name='vm_start'),
    url(r'^vm/stop/(?P<id>\d+)/$', 'cluster.views.vm_stop', name='vm_stop'),
    url(r'^vm/add/$', 'cluster.views.vms', name='vm_add'),    
    url(r'^vm/migrate/(?P<vmid>\d+)/(?P<destnode>\w+)/$', 'cluster.views.vm_migrate', name='vm_migrate'),    

	url(r'^loadbalance/$', 'cluster.views.loadbalance', name='loadbalance'),

)
