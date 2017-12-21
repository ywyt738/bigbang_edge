from django.conf.urls import url
from . import views as home_views

urlpatterns = [
    url(r'^$', home_views.index, name='resources'),
    url(r'hosts/$', home_views.hosts, name='hosts'),
    url(r'hosts.json$', home_views.hostsJson, name='hostsJson'),
    url(r'hosts/add/$', home_views.new_add, name='add'),
    url(r'hosts/(?P<host_id>[^/]+)/$', home_views.host_detail, name='host_detail'),
    url(r'hosts/(?P<host_id>[^/]+)/(?P<status>[^/]+)/$', home_views.host_detail, name='host_change'),
    url(r'ip_resources/$', home_views.ip_resources, name='ip_resources'),
    url(r'ip_resources/add_network/$', home_views.ip_resources, name='add_network'),
    url(r'ip.json$', home_views.ipJson, name='IPJson'),
    url(r'svn_add/$', home_views.svn_apply, name='svn'),
    url(r'svn_list/$', home_views.svn_list, name='snv_list'),
    url(r'svn_project_check/$', home_views.svn_project_check, name='svn_check'),
    url(r'account/$', home_views.account, name='account'),
]
