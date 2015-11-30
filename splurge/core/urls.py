from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
                       url(r'^login/', 'login', name='login'),
                       url(r'^signup/', 'signup', name='signup'),
                       url(r'^homepage/', 'homepage', name='homepage'),
                       url(r'^employees/', 'employees', name='employees'),
                       url(r'^teams/', 'teams', name='teams'),
                       url(r'^add_employee/', 'add_employee', name='add_employee'),
                       url(r'^create_card_for_employee/(?P<employee_id>[\-\w]+)$', 'create_card_for_employee',
                           name='create_card_for_employee'),
                       url(r'^delete_employee/(?P<employee_id>[\-\w]+)$', 'delete_employee', name='delete_employee'),
                       url(r'^create_team/', 'create_team', name='create_team'),
                       url(r'^create_card_for_team/(?P<team_id>[\-\w]+)$', 'create_card_for_team',
                           name="create_card_for_team"),
                       url(r'^activate_user/(?P<unique_id>[\-\w]+)/$', 'activate_user', name='activate_user'),
                       url(r'^$', 'home', name='home'),
                       )
