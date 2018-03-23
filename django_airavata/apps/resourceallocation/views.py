import datetime
import time
from django.shortcuts import render, redirect
from airavata.model.security.ttypes import AuthzToken
from django.conf import settings
from allocation_manager_models.ttypes import UserAllocationDetail, ReviewerSpecificResourceDetail
from allocation_manager_models.ttypes import ReviewerAllocationDetail
from allocation_manager_models.ttypes import UserSpecificResourceDetail
import logging
logger = logging.getLogger(__name__)


def admin(request):
    try:
        authz_token = AuthzToken("")
        gateway_id = settings.GATEWAY_ID
        group_id = "reviewers"
        if (request.method == 'POST'):
            selectedReviewers = request.POST.getlist('selectedReviewers')
            projectId = int(request.POST['projectId'])

            #Assign reviwers to the project
            for reviewerId in selectedReviewers:
                request.allocation_manager_client.assignReviewers(authz_token,projectId, reviewerId, "admin")

        details = request.allocation_manager_client.getAllRequestsForAdmin(authz_token,"admin")
        reviewerDetailsList = []
        for detail in details:
            #members = request.sharing_client.getGroupMembersOfTypeUser(gateway_id, group_id, 0, -1)
            #print(members)
            allReviewersList = ['reviewer1','reviewer2']
            assignedReviewerDetails = request.allocation_manager_client.getAllAssignedReviewersForRequest(authz_token,
                detail.projectId)
            allAssignedReviewerList= []
            for reviewer in assignedReviewerDetails:
                allAssignedReviewerList.append(reviewer.reviewerUsername)
            unassignedReviewersList = list(set(allReviewersList) - set(allAssignedReviewerList))
            reviewerDetailsList.append(unassignedReviewersList)
        return render(request, 'dashboard/admin.html',
                      {'all_requests': details, 'reviewerDetailsList': reviewerDetailsList})

    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

def AdminRequestView(request):
    authz_token = AuthzToken("")
    projectId = int(request.GET.get('projectId'))
    projectReviewList = request.allocation_manager_client.getAllReviewsForARequest(authz_token,projectId)
    reviewerReview = ReviewerAllocationDetail()
    userSubmittedDetails = request.allocation_manager_client.getAllocationRequest(authz_token,projectId)
    userSpecificDetailsList = request.allocation_manager_client.getUserSpecificResource(authz_token, projectId)
    specificDetails = request.allocation_manager_client.getReviewerSpecificResource(authz_token, projectId)
    reviewerSpecificDetailsList = []
    selectedReviewer = ''

    if (request.method == 'POST'):
        s = request.POST.get('start')
        rejectionReason = request.POST.get('reject-reason')
        specificResource = request.POST.get('specific-resource')
        startDate = None
        if s is not None:
            startDate = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
            s = request.POST.get('end')
            endDate = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
            serviceUnits = request.POST.get('allocation-units')

        if(startDate is not None):
            request.allocation_manager_client.approveRequest(authz_token,projectId,"admin",int(startDate),int(endDate),int(serviceUnits),specificResource)
            return redirect('/resourceallocation/admin')
        if rejectionReason is not None:
            request.allocation_manager_client.rejectRequest(authz_token,projectId,"admin",rejectionReason,specificResource)
            return redirect('/resourceallocation/admin')
        selectedReviewer = request.POST.get('selectedReviewer')
        for review in projectReviewList:
            if(review.username == selectedReviewer):
                reviewerReview = review

        for review in specificDetails:
            if (review.username == selectedReviewer):
                reviewerSpecificDetailsList.append(review)

    assignedReviewersList = request.allocation_manager_client.getAllAssignedReviewersForRequest(authz_token,projectId)
    return render(request, 'dashboard/admin-request-view.html',
                  {'userSubmittedDetails': userSubmittedDetails,
                   'assignedReviewersList': assignedReviewersList,
                   'reviewerReview': reviewerReview, 'selectedReviewer': selectedReviewer,'userSpecificDetailsList': userSpecificDetailsList,
                   'reviewerSpecificDetailsList':reviewerSpecificDetailsList})

def ReviewerView(request):
    try:
        authz_token = AuthzToken("")
        details = request.allocation_manager_client.getAllRequestsForReviewers(authz_token,"reviewer2")
        reviewerId = "reviewer2"
        return render(request, 'dashboard/reviewer.html', {
            'all_requests': details, 'reviewerId':reviewerId
        })
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

def ReviewerRequestView(request):
    authz_token = AuthzToken("")
    projectId = int(request.GET.get('projectId'))
    reviewerId = request.GET.get('reviewerId')
    reviewerReview = ReviewerAllocationDetail()
    reviewerSpecificDetailsList = []
    userSubmittedDetails = request.allocation_manager_client.getAllocationRequest(authz_token,projectId)
    userSpecificDetailsList = request.allocation_manager_client.getUserSpecificResource(authz_token,projectId)
    specificDetails = request.allocation_manager_client.getReviewerSpecificResource(authz_token, projectId)
    reviewsList = request.allocation_manager_client.getAllReviewsForARequest(authz_token,projectId)

    for review in reviewsList:
        if(review.username == reviewerId):
            reviewerReview = review

    #For extracting reviewer specific resource
    for review in specificDetails:
        if(review.username == reviewerId):
            reviewerSpecificDetailsList.append(review)

    if (request.method == 'POST'):
        reqObj = ReviewerAllocationDetail()
        reqObj.projectId = projectId
        reqObj.reviewDate = int(datetime.datetime.now().strftime("%s")) * 1000
        reqObj.diskUsageRangePerJob = int(request.POST['diskUsage'])
        reqObj.maxMemoryPerCpu = int(request.POST['maxMemoryPerCpu'])
        reqObj.numberOfCpuPerJob = int(request.POST['numberOfCpuPerJob'])
        reqObj.typicalSuPerJob = int(request.POST['typicalSuPerJob'])
        #reqObj.documents = int(request.POST['documents'])
        reqObj.username = reviewerId
        request.allocation_manager_client.updateRequestByReviewer(authz_token,reqObj)
        for i in range(0, len(request.POST.getlist('specificResources'))):
            reviewerSpecObj = ReviewerSpecificResourceDetail()
            reviewerSpecObj.projectId = int(projectId)
            reviewerSpecObj.comments = request.POST.getlist('comments')[i]
            reviewerSpecObj.applicationsToBeUsed = ",".join(request.POST.getlist('application' + str(i + 1)))
            if request.POST.getlist('allocation')[i]!='':
                reviewerSpecObj.reviewedServiceUnits = int(request.POST.getlist('allocation')[i])
            reviewerSpecObj.resourceType = request.POST.getlist('resourceType')[i]
            reviewerSpecObj.specificResource = request.POST.getlist('specificResources')[i]
            reviewerSpecObj.username = reviewerId
            reviewerSpecificDetailsList.append(reviewerSpecObj)
        request.allocation_manager_client.updateReviewerSpecificResource(authz_token, int(projectId), reviewerSpecificDetailsList)

        return redirect('/resourceallocation/reviewer')
    return render(request, 'dashboard/reviewer-request-view.html',
                  {'userSubmittedDetails': userSubmittedDetails,
                   'reviewerReview': reviewerReview, 'userSpecificDetailsList': userSpecificDetailsList,
                   'reviewerSpecificDetailsList':reviewerSpecificDetailsList})

#@login_required
def index(request):

    try:
        #authz_token = request.authz_token
        authz_token = AuthzToken("")
        details = request.allocation_manager_client.getAllRequestsForAdmin(authz_token,"admin")
        details_specific = request.allocation_manager_client.getUserSpecificResource(authz_token,details[0].projectId)
        return render(request, 'dashboard/index.html', {
            'all_requests': details,'all_requests_specific':details_specific
        })
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

def requestCreate(request):

    try:
        authz_token = AuthzToken("")
        projectId = request.GET.get('projectId')
        projectDetails = UserAllocationDetail()
        userSpecificDetails = []

        reqSpecificList = []
        '''Get the project details for an existing request'''
        if(projectId is not None):
            projectDetails = request.allocation_manager_client.getAllocationRequest(authz_token,int(projectId))
            userSpecificDetails = request.allocation_manager_client.getUserSpecificResource(authz_token, int(projectId))

        if(request.method=='POST'):
            reqObj = UserAllocationDetail();

            if(projectId is not None):
                reqObj.projectId = int(projectId)

            reqObj.title = request.POST['title']
            reqObj.requestedDate = int(datetime.datetime.now().strftime("%s"))*1000
            reqObj.projectDescription = request.POST['description']
            reqObj.keywords = request.POST['keywords']
            reqObj.diskUsageRangePerJob = int(request.POST['diskUsage'])
            reqObj.maxMemoryPerCpu = int(request.POST['memorycpu'])
            reqObj.numberOfCpuPerJob = int(request.POST['cpuPerJob'])
            reqObj.typicalSuPerJob = int(request.POST['typicalSu'])
            reqObj.comments = request.POST['comments']
            reqObj.username = "admin"

            oldLen = len(userSpecificDetails)
            for i in range(0, len(request.POST.getlist('specificResources'))):
                if(i >= oldLen):
                    userSpecObj = UserSpecificResourceDetail()
                    if (projectId is not None):
                        userSpecObj.projectId = int(projectId)
                    userSpecObj.applicationsToBeUsed = ",".join(request.POST.getlist('application' + str(i + 1)))
                    userSpecObj.requestedServiceUnits = int(request.POST.getlist('allocation')[i])
                    userSpecObj.resourceType = request.POST.getlist('resourceType')[i]
                    userSpecObj.specificResource = request.POST.getlist('specificResources')[i]
                    reqSpecificList.append(userSpecObj)
                else:
                    userSpecificDetails[i].applicationsToBeUsed = ",".join(request.POST.getlist('application' + str(i + 1)))
                    userSpecificDetails[i].requestedServiceUnits = int(request.POST.getlist('allocation')[i])
                    userSpecificDetails[i].resourceType = request.POST.getlist('resourceType')[i]
                    userSpecificDetails[i].specificResource = request.POST.getlist('specificResources')[i]
                    reqSpecificList.append(userSpecificDetails[i])

            if (projectId is not None):
                request.allocation_manager_client.updateAllocationRequest(authz_token,reqObj)
                request.allocation_manager_client.updateUserSpecificResource(authz_token,int(projectId),reqSpecificList)
            else:
                createdProjectId = request.allocation_manager_client.createAllocationRequest(authz_token,reqObj)
                for i in range(0, len(reqSpecificList)):
                    reqSpecificList[i].projectId = createdProjectId
                    request.allocation_manager_client.createUserSpecificResource(authz_token, reqSpecificList[i])
            return redirect('/resourceallocation')
        else:
            return render(request, 'dashboard/request_form.html',
                          {'projectDetails': projectDetails,'projectSpecificDetails':userSpecificDetails})
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')