from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
                       url(r'^login/', 'login', name='login'),
                       url(r'^signup/', 'signup', name='signup'),
                       url(r'^homepage/', 'homepage', name='homepage'),
                       url(r'^$', 'home', name='home'),
                   )