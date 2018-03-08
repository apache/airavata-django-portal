import datetime
import itertools
import time
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
from allocation_manager_models.ttypes import ReviewerAllocationDetail
import logging
logger = logging.getLogger(__name__)


def admin(request):
    try:
        if (request.method == 'POST'):
            selectedReviewers = request.POST.getlist('selectedReviewers')
            projectId = request.POST['projectId']

            #Assign reviwers to the project
            for reviewerId in selectedReviewers:
                request.allocation_manager_client.assignReviewers(projectId, reviewerId, "admin")

        details = request.allocation_manager_client.getAllRequestsForAdmin("admin")
        reviewerDetailsList = []
        for detail in details:
            reviewerDetails = request.allocation_manager_client.getAllUnassignedReviewersForRequest(
                detail.projectId)
            reviewerDetailsList.append(reviewerDetails)
        return render(request, 'dashboard/admin.html',
                      {'all_requests': details, 'reviewerDetailsList': reviewerDetailsList})

    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

def AdminRequestView(request):

    projectId = request.GET.get('projectId')
    projectReviewList = request.allocation_manager_client.getAllReviewsForARequest(projectId)
    reviewerReview = ReviewerAllocationDetail()
    userSubmittedDetails = request.allocation_manager_client.getAllocationRequest(projectId)
    print(projectReviewList)
    selectedReviewer = ''
    if (request.method == 'POST'):
        s = request.POST.get('start')
        rejecttionReason = request.POST.get('reject-reason')
        startDate = None
        if s is not None:
            startDate = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
            s = request.POST.get('end')
            endDate = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
            serviceUnits = request.POST.get('allocation-units')
        if(startDate is not None):
            request.allocation_manager_client.approveRequest(projectId,"admin",int(startDate),int(endDate),int(serviceUnits))
            return redirect('/resourceallocation/admin')
        if rejecttionReason is not None:
            request.allocation_manager_client.rejectRequest(projectId,"admin")
            return redirect('/resourceallocation/admin')
        selectedReviewer = request.POST.get('selectedReviewer')
        print(selectedReviewer)
        for review in projectReviewList:
            if(review.username == selectedReviewer):
                reviewerReview = review


    allReviewersList = request.allocation_manager_client.getAllReviewers()
    UnassignedReviewersList = request.allocation_manager_client.getAllUnassignedReviewersForRequest(projectId)
    assignedReviewersList = [x for x in allReviewersList + UnassignedReviewersList if x not in allReviewersList or x not in UnassignedReviewersList]

    print(selectedReviewer)
    return render(request, 'dashboard/admin-request-view.html',
                  {'userSubmittedDetails': userSubmittedDetails,
                   'assignedReviewersList': assignedReviewersList,
                   'reviewerReview': reviewerReview, 'selectedReviewer': selectedReviewer})

def ReviewerView(request):
    try:
        details = request.allocation_manager_client.getAllRequestsForReviewers("reviewer2")
        reviewerId = "reviewer2"
        return render(request, 'dashboard/reviewer.html', {
            'all_requests': details, 'reviewerId':reviewerId
        })
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

def ReviewerRequestView(request):

    projectId = request.GET.get('projectId')
    reviewerId = request.GET.get('reviewerId')
    '''projectReviewList = request.allocation_manager_client.getAllReviewsForARequest(projectId)'''
    reviewerReview = ReviewerAllocationDetail()

    userSubmittedDetails = request.allocation_manager_client.getAllocationRequest(projectId)
    reviewsList = request.allocation_manager_client.getAllReviewsForARequest(projectId)

    for review in reviewsList:
        if(review.username == reviewerId):
            reviewerReview = review

    if (request.method == 'POST'):
        reqObj = ReviewerAllocationDetail()
        reqObj.projectId = projectId
        reqObj.requestedDate = int(datetime.datetime.now().strftime("%s")) * 1000
        reqObj.typeOfAllocation = request.POST['allocationType']
        reqObj.applicationsToBeUsed = ",".join(request.POST.getlist('application'))
        reqObj.keywords = request.POST['keywords']
        reqObj.diskUsageRangePerJob = int(request.POST['diskUsage'])
        reqObj.maxMemoryPerCpu = int(request.POST['maxMemoryPerCpu'])
        reqObj.numberOfCpuPerJob = int(request.POST['numberOfCpuPerJob'])
        reqObj.typicalSuPerJob = int(request.POST['numberOfCpuPerJob'])
        reqObj.serviceUnits = int(request.POST['numberOfCpuPerJob'])
        reqObj.username = reviewerId

        print(reqObj)
        request.allocation_manager_client.updateRequestByReviewer(reqObj)
        return redirect('/resourceallocation/reviewer')

    return render(request, 'dashboard/reviewer-request-view.html',
                  {'userSubmittedDetails': userSubmittedDetails,
                   'reviewerReview': reviewerReview})

def index(request):

    try:
        details = request.allocation_manager_client.getAllRequestsForAdmin("admin")
        return render(request, 'dashboard/index.html', {
            'all_requests': details
        })
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

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

    try:
        projectId = request.GET.get('projectId')
        status = request.GET.get('status')
        projectDetails = UserAllocationDetail()

        '''Get the project details for an existing request'''
        if(projectId is not None):
            projectDetails = request.allocation_manager_client.getAllocationRequest(projectId)
            print(projectDetails)

        if(request.method=='POST'):
            reqObj = UserAllocationDetail();

            if(projectId is not None):
                reqObj.projectId = projectId
            else:
                reqObj.projectId = "6";

            reqObj.title = request.POST['title']
            reqObj.requestedDate = int(datetime.datetime.now().strftime("%s"))*1000
            reqObj.projectDescription = request.POST['description']
            reqObj.typeOfAllocation = request.POST['allocationType']
            reqObj.applicationsToBeUsed = ",".join(request.POST.getlist('application'))
            reqObj.keywords = request.POST['keywords']
            reqObj.diskUsageRangePerJob = int(request.POST['diskUsage'])
            reqObj.maxMemoryPerCpu = int(request.POST['memorycpu'])
            reqObj.numberOfCpuPerJob = int(request.POST['cpuPerJob'])
            reqObj.typicalSuPerJob = int(request.POST['typicalSu'])
            reqObj.serviceUnits = int(request.POST['allocation'])
            reqObj.specificResourceSelection = request.POST['resourceType']
            reqObj.username = "admin"

            if (projectId is not None):
                request.allocation_manager_client.updateAllocationRequest(reqObj)
            else:
                request.allocation_manager_client.createAllocationRequest(reqObj)
            return redirect('/resourceallocation')
        else:
            return render(request, 'dashboard/request_form.html',
                          {'projectDetails': projectDetails})
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