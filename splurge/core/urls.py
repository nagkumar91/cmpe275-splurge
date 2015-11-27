from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
                       url(r'^login/', 'login', name='login'),
                       url(r'^signup/', 'signup', name='signup'),
                       url(r'^homepage/', 'homepage', name='homepage'),
                       url(r'^activate_user/(?P<unique_id>[\-\w]+)/$', 'activate_user', name='activate_user'),
                       url(r'^$', 'home', name='home'),
                   )