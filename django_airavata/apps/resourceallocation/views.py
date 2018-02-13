import datetime

from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from rest_framework.renderers import JSONRenderer

from .forms import UserForm, RequestCreateForm
from django.conf import settings
from .models import Request
from django.core import serializers
from allocation_manager_models.ttypes import UserAllocationDetail
import logging
logger = logging.getLogger(__name__)


def admin(request):
    #user = request.user.username

    try:
        details = request.allocation_manager_client.getAllRequestsForAdmin("admin")
        #print(details[0].projectId)
        reviewerDetailsList = []
        for detail in details:
            reviewerDetails = request.allocation_manager_client.getAllUnassignedReviewersForRequest(detail.projectId)
            reviewerDetailsList.append(reviewerDetails)
        #print(details)
        #print(reviewerDetailsList)
        return render(request, 'dashboard/admin.html', {'all_requests': details,'reviewerDetailsList':reviewerDetailsList})
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('dashboard/index.html')

def index(request):
    #user = request.user.username

    try:
        details = request.allocation_manager_client.getAllRequestsForAdmin("admin")
        return render(request, 'dashboard/index.html', {
            'all_requests': details
        })
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('dashboard/index.html')

'''class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'all_requests'

    def get_queryset(self):
        try:
            details = request.allocation_manager_client.getAllRequestsForAdmin(user)
         render(request, 'dashboard/index.html', {
                'all_requests': details
            })
        except Exception as e:
            logger.exception("Failed to load the group details")
            return redirect('/groups')
'''

class ReviewerView(generic.ListView):
    template_name = 'dashboard/reviewer.html'
    context_object_name = 'all_requests'

    def get_queryset(self):
        return Request.objects.all()




class AdminRequestView(generic.ListView):
    model = Request
    template_name = 'dashboard/admin-request-view.html'

class DetailView(generic.DetailView):
    model = Request
    template_name = 'dashboard/detail.html'


'''class RequestCreate(CreateView):
    model = Request
    fields = ['request_title', 'request_status', 'request_description', 'allocation_type',
              'applications_to_be_used', 'disk_usage_range_per_job', 'document', 'field_of_science',
              'keywords', 'max_memory_per_cpu', 'num_cpus_per_job', 'request_reviewed_and_funded_by',
              'request_date', 'service_units', 'specific_resource_selection', 'typical_su_per_job'] '''

def requestCreate(request):
    print("here requestCreate")
    user = request.user.username
    fields = ['request_title', 'request_status', 'request_description', 'allocation_type',
              'applications_to_be_used', 'disk_usage_range_per_job', 'document', 'field_of_science',
              'keywords', 'max_memory_per_cpu', 'num_cpus_per_job', 'request_reviewed_and_funded_by',
              'request_date', 'service_units', 'specific_resource_selection', 'typical_su_per_job']
    try:
        if(request.method=='POST'):
            reqObj = UserAllocationDetail();
            reqObj.projectId = "12345678";
            reqObj.title = request.POST['title']
            reqObj.requestedDate = int(datetime.datetime.now().strftime("%s"))*1000
            reqObj.projectDescription = request.POST['description']
            reqObj.typeOfAllocation = request.POST['allocationType']
            reqObj.username = "admin"
            details = request.allocation_manager_client.createAllocationRequest(reqObj)
            print(details)
            return redirect('/resourceallocation')
        else:
            return render(request, 'dashboard/request_form.html')
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

class RequestUpdate(UpdateView):
    model = Request
    fields = ['request_title', 'request_status', 'request_description', 'allocation_type',
              'applications_to_be_used', 'disk_usage_range_per_job', 'document', 'field_of_science',
              'keywords', 'max_memory_per_cpu', 'num_cpus_per_job', 'request_reviewed_and_funded_by',
              'request_date', 'service_units', 'specific_resource_selection', 'typical_su_per_job']

class RequestDelete(DeleteView):
    model = Request
    success_url = reverse_lazy('dashboard:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'dashboard/registration_form.html'


    # Display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard:index')
        return render(request, self.template_name, {'form': form})



