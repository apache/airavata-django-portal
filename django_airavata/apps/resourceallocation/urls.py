from django.conf.urls import url
from . import views

app_name ='dashboard'

urlpatterns = [
    # /dashboard/
    # url(r'^$', views.index, name='index'),
    #url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^$', views.index, name="index"),
    # /dashboard/reviewer
   url(r'^reviewer/$', views.ReviewerView.as_view(), name='reviewer'),


    # /dashboard/admin
    url(r'^admin/$', views.AdminView.as_view(), name='admin'),

    # /dashboard/admin/141
    url(r'^admin/request-view/$', views.AdminRequestView.as_view(), name='admin-request-view'),



    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /dashboard/712/
    # url(r'^(?P<request_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),


    # /dashboard/request/add
    url(r'^request/add/$', views.requestCreate, name='request-add'),

    # /dashboard/request/2/
    url(r'^request/(?P<pk>[0-9]+)/$', views.RequestUpdate.as_view(), name='request-update'),

    # /dashboard/request/2/delete/
    url(r'^request/(?P<pk>[0-9]+)/delete/$', views.RequestDelete.as_view(), name='request-delete'),
]