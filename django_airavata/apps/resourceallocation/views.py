import datetime
import time
import json
from django.shortcuts import render, redirect
from airavata.model.security.ttypes import AuthzToken
from django.contrib.auth.decorators import login_required
from django.conf import settings
from allocation_manager_models.ttypes import UserAllocationDetail, ReviewerSpecificResourceDetail
from allocation_manager_models.ttypes import ReviewerAllocationDetail
from allocation_manager_models.ttypes import UserSpecificResourceDetail
import logging
from django_airavata.apps.api import serializers
from django_airavata.apps.api.views import ApplicationModuleViewSet
logger = logging.getLogger(__name__)

class appDeployment:
    appDeploymentId = ""
    appModuleId = ""

    def function(self):
        print("This is a message inside the class.")

@login_required
def admin(request):
    try:
        authz_token = request.authz_token
        loggedinUser = authz_token.claimsMap['userName']
        reviewerGroup = request.profile_service['group_manager'].getGroup(authz_token, settings.REVIEWER_GROUP_ID)
        allReviewersList = []
        loggedinUserGroups = getLoggedInRoles(request)
        if('admin' not in loggedinUserGroups):
            return redirect('/resourceallocation')

        for reviewer in reviewerGroup.members:
            allReviewersList.append(reviewer.split('@')[0])
        if (request.method == 'POST'):
            selectedReviewers = request.POST.getlist('selectedReviewers')
            projectId = int(request.POST['projectId'])

            #Assign reviwers to the project
            for reviewerId in selectedReviewers:
                request.allocation_manager_client.assignReviewers(authz_token,projectId, reviewerId, loggedinUser)

        details = request.allocation_manager_client.getAllRequests(authz_token,loggedinUser, "admin")
        reviewerDetailsList = []
        for detail in details:
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

@login_required
def AdminRequestView(request):
    authz_token = request.authz_token
    loggedinUser = authz_token.claimsMap['userName']
    projectId = int(request.GET.get('projectId'))
    projectReviewList = request.allocation_manager_client.getAllReviewsForARequest(authz_token, projectId)
    reviewerReview = ReviewerAllocationDetail()
    userSubmittedDetails = request.allocation_manager_client.getAllocationRequest(authz_token, projectId)
    userSpecificDetailsList = request.allocation_manager_client.getUserSpecificResource(authz_token, projectId)
    specificDetails = request.allocation_manager_client.getReviewerSpecificResource(authz_token, projectId)
    applications = request.airavata_client.getAllAppModules(authz_token, settings.GATEWAY_ID)
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

        if (startDate is not None):
            request.allocation_manager_client.approveRequest(authz_token, projectId, loggedinUser, int(startDate),
                                                             int(endDate), int(serviceUnits), specificResource)
            return redirect('/resourceallocation/admin')
        if rejectionReason is not None:
            request.allocation_manager_client.rejectRequest(authz_token, projectId, loggedinUser, rejectionReason,
                                                            specificResource)
            return redirect('/resourceallocation/admin')
        selectedReviewer = request.POST.get('selectedReviewer')
        for review in projectReviewList:
            if (review.username == selectedReviewer):
                reviewerReview = review
        print(specificDetails)
        for review in specificDetails:
            if (review.username == selectedReviewer):
                reviewerSpecificDetailsList.append(review)

    assignedReviewersList = request.allocation_manager_client.getAllAssignedReviewersForRequest(authz_token, projectId)
    return render(request, 'dashboard/admin-request-view.html',
                  {'userSubmittedDetails': userSubmittedDetails,
                   'assignedReviewersList': assignedReviewersList,
                   'reviewerReview': reviewerReview, 'selectedReviewer': selectedReviewer,
                   'userSpecificDetailsList': userSpecificDetailsList,
                   'reviewerSpecificDetailsList': reviewerSpecificDetailsList,
                   'applications': applications})

@login_required
def ReviewerView(request):
    try:
        authz_token = request.authz_token
        loggedinUser = authz_token.claimsMap['userName']

        loggedinUserGroups = getLoggedInRoles(request)
        if ('reviewer' not in loggedinUserGroups):
            return redirect('/resourceallocation')

        details = request.allocation_manager_client.getAllRequestsForReviewers(authz_token,loggedinUser)
        return render(request, 'dashboard/reviewer.html', {
            'all_requests': details, 'reviewerId':loggedinUser
        })
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

@login_required
def ReviewerRequestView(request):
    authz_token = request.authz_token
    loggedinUser = authz_token.claimsMap['userName']
    projectId = int(request.GET.get('projectId'))
    reviewerId = loggedinUser
    reviewerReview = ReviewerAllocationDetail()
    reviewerSpecificDetailsList = []
    userSubmittedDetails = request.allocation_manager_client.getAllocationRequest(authz_token,projectId)
    userSpecificDetailsList = request.allocation_manager_client.getUserSpecificResource(authz_token,projectId)
    specificDetails = request.allocation_manager_client.getReviewerSpecificResource(authz_token, projectId)
    reviewsList = request.allocation_manager_client.getAllReviewsForARequest(authz_token,projectId)
    applications = request.airavata_client.getAllAppModules(authz_token, settings.GATEWAY_ID)
    print(applications)
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
        if request.POST['diskUsage'] is not '': reqObj.diskUsageRangePerJob = int(request.POST['diskUsage'])
        if request.POST['maxMemoryPerCpu'] is not '': reqObj.maxMemoryPerCpu = int(request.POST['maxMemoryPerCpu'])
        if request.POST['numberOfCpuPerJob'] is not '': reqObj.numberOfCpuPerJob = int(request.POST['numberOfCpuPerJob'])
        if request.POST['typicalSuPerJob'] is not '': reqObj.typicalSuPerJob = int(request.POST['typicalSuPerJob'])
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
                   'reviewerSpecificDetailsList':reviewerSpecificDetailsList,
                   'applications': applications})

@login_required
def index(request):


    try:
        authz_token = request.authz_token
        loggedinUser = authz_token.claimsMap['userName']
        loggedinUserGroups = getLoggedInRoles(request)
        if len(loggedinUserGroups) == 0:
            return redirect('/resourceallocation/unauthorized')
        if len(loggedinUserGroups) > 1:
            #change this later
            loggedinUserGroup = loggedinUserGroups[0]
        else:
            loggedinUserGroup = loggedinUserGroups[0]
        if loggedinUserGroup == 'user':
            details = request.allocation_manager_client.getAllRequests(authz_token,loggedinUser, 'user')
            details_specific = []
            if len(details) > 0:
                details_specific = request.allocation_manager_client.getUserSpecificResource(authz_token,details[0].projectId)
            return render(request, 'dashboard/index.html', {
            'all_requests': details,'all_requests_specific':details_specific
            })
        elif loggedinUserGroup == 'admin':
            return redirect('/resourceallocation/admin')
        elif loggedinUserGroup == 'reviewer':
            return redirect('/resourceallocation/reviewer')

    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

@login_required
def requestCreate(request):
    try:
        authz_token = request.authz_token
        loggedinUser = authz_token.claimsMap['userName']
        projectId = request.GET.get('projectId')
        projectDetails = UserAllocationDetail()
        userSpecificDetails = []
        applications = request.airavata_client.getAllAppModules(authz_token, settings.GATEWAY_ID)
        all_deployments = request.airavata_client.getAllApplicationDeployments(authz_token, settings.GATEWAY_ID)
        serializer = serializers.ApplicationDeploymentDescriptionSerializer(all_deployments, many=True,
                                                                          context={'request': request})

        all_deployments = json.dumps(serializer.data)
        reqSpecificList = []
        '''Get the project details for an existing request'''
        if(projectId is not None):
            projectDetails = request.allocation_manager_client.getAllocationRequest(authz_token,int(projectId))
            userSpecificDetails = request.allocation_manager_client.getUserSpecificResource(authz_token, int(projectId))
            if(loggedinUser != projectDetails.username):
                return redirect('/resourceallocation')

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
            reqObj.username = loggedinUser

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

            for i in range(0, len(reqSpecificList)):
                if reqSpecificList[i].requestedServiceUnits < settings.AUTO_APPROVE_THRESHOLD :
                    # call compute resource for each specific resource and see if asked allocation exists
                    resourceExists = True
                    if(resourceExists):
                        request.allocation_manager_client.approveRequest(authz_token,reqSpecificList[i].projectId,"auto",0,0,
                                                                     reqSpecificList[i].requestedServiceUnits,reqSpecificList[i].specificResource)
            return redirect('/resourceallocation')
        else:
            canSubmit = request.allocation_manager_client.canSubmitRequest(authz_token, loggedinUser)
            return render(request, 'dashboard/request_form.html',
                          {'projectDetails': projectDetails,'projectSpecificDetails':userSpecificDetails,
                           'canSubmit': canSubmit, 'projectId':projectId,'applications':applications,
                           'all_deployments':all_deployments, 'allDeploys':serializer.data})
    except Exception as e:
        logger.exception("Failed to load resource allocation details")
        return redirect('/resourceallocation')

def unauthorized(request):
    return render(request, 'dashboard/unauthorized.html')

def getLoggedInRoles(request):
    authz_token = request.authz_token
    loggedinUser = authz_token.claimsMap['userName']
    loggedinUserGroups = []

    adminGroup = request.profile_service['group_manager'].getGroup(authz_token, settings.ADMIN_GROUP_ID)
    reviewerGroup = request.profile_service['group_manager'].getGroup(authz_token, settings.REVIEWER_GROUP_ID)
    userGroup = request.profile_service['group_manager'].getGroup(authz_token, settings.USER_GROUP_ID)
    if (loggedinUser + '@' + settings.GATEWAY_ID in adminGroup.members):
        loggedinUserGroups.append('admin')
    if (loggedinUser + '@' + settings.GATEWAY_ID in reviewerGroup.members):
        loggedinUserGroups.append('reviewer')
    if (loggedinUser + '@' + settings.GATEWAY_ID in userGroup.members):
        loggedinUserGroups.append('user')

    return loggedinUserGroups
