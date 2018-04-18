from django.conf.urls import url
from . import views

app_name ='dashboard'

urlpatterns = [
    # /dashboard/
    url(r'^$', views.index, name="index"),
    # /dashboard/reviewer
   url(r'^reviewer/$', views.ReviewerView, name='reviewer'),

    # /dashboard/admin
    url(r'^admin/$', views.admin, name='admin'),

    # /dashboard/admin/141
    url(r'^admin/request-view/$', views.AdminRequestView, name='admin-request-view'),

    # /dashboard/reviewer/141
    url(r'^reviewer/request-view/$', views.ReviewerRequestView, name='reviewer-request-view'),

    # /dashboard/request/add
    url(r'^request/add/$', views.requestCreate, name='request-add'),

    #/dashboard/unauthorized
    url(r'^unauthorized/$', views.unauthorized, name='unauthorized'),
]