# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.renderers import JSONRenderer

from .forms import CreateForm, AddForm, RemoveForm
from django.contrib import messages
from airavata.model.sharing.ttypes import UserGroup
from airavata.model.sharing.ttypes import GroupCardinality
import datetime
import uuid

import logging

logger = logging.getLogger(__name__)


@login_required
def groups_manage(request):

    request.active_nav_item = "manage"
    gateway_id = settings.GATEWAY_ID
    username = request.user.username
    authz_token = request.authz_token

    try:
        owner_list = request.profile_service['group_manager'].getAllGroupsUserBelongs(authz_token, username)
        # for group in owner_list:
        #     if group.groupCardinality == 0:
        #         owner_list.remove(group)
        # owner = []
        # for group in owner_list:
        #     if group.ownerId == username:
        #         owner.append(group)

        owner = JSONRenderer().render(owner_list)

        member_list = request.profile_service['group_manager'].getAllGroupsUserBelongs(authz_token, username)
        # member = []
        # for group in member_list:
        #     if group.ownerId != username:
        #         member.append(group)

        member = JSONRenderer().render(member_list)

        return render(request, 'django_airavata_groups/groups_manage.html', {
            'groups_owners_data': owner, 'groups_members_data': member
        })

    except:
        logger.exception("Failed to load the Manage Groups page")
        return redirect('/')

@login_required
def groups_create(request):

    gateway_id = settings.GATEWAY_ID
    username = request.user.username
    #If role = user
    group_type = 1
    #Else if role = admin
    #group_type = 2
    group_cardinality = GroupCardinality.MULTI_USER

    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES, initial={'domain_id': gateway_id, 'group_owner': username, 'group_type': group_type, 'group_cardinality': group_cardinality})
        if form.is_valid():
            group_name = form.cleaned_data.get('group_name').replace(" ","-").lower()
            group_id = group_name + str(uuid.uuid4().hex)
            group = UserGroup(groupId=group_id, domainId=gateway_id, name=form.cleaned_data.get('group_name'), description=form.cleaned_data.get('description'), ownerId=username, groupType=group_type, groupCardinality=group_cardinality, createdTime=None, updatedTime=None)
            try:
                create = request.sharing_client.createGroup(group)
                messages.success(request, 'Group '+group_id+' has been created successfully!')
                return redirect('/groups')
            except Exception as e:
                logger.exception("Failed to create the group")
                return redirect('/groups')

    else:
        form = CreateForm(initial={'domain_id': gateway_id, 'group_owner': username, 'group_type': group_type, 'group_cardinality': group_cardinality})

    return render(request, 'django_airavata_groups/groups_create.html', {
        'form': form
    })

@login_required
def view_group(request):

    gateway_id = settings.GATEWAY_ID
    group_id = request.GET.get('group_id')
    user = request.user.username

    try:
        details = request.sharing_client.getGroup(gateway_id, group_id)
        members = request.sharing_client.getGroupMembersOfTypeUser(gateway_id, group_id, 0, -1)
        c_time = datetime.datetime.fromtimestamp(details.createdTime/1000.0)
        u_time = datetime.datetime.fromtimestamp(details.updatedTime/1000.0)
        return render(request, 'django_airavata_groups/group_details.html', {
            'group': details, 'c_time': c_time, 'u_time': u_time, 'members': members, 'u_id': user
        })
    except Exception as e:
        logger.exception("Failed to load the group details")
        return redirect('/groups')


@login_required
def edit_group(request, group_id):

    return render(request, 'django_airavata_groups/group_edit.html', {
        'group_id': group_id,
    })


@login_required
def delete_group(request):

    gateway_id = settings.GATEWAY_ID
    group_id = request.GET.get('group_id')

    try:
        delete = request.sharing_client.deleteGroup(gateway_id, group_id)
        messages.success(request, 'Group '+group_id+' has been deleted successfully!')
        return redirect('/groups')
    except Exception as e:
        logger.exception("Failed to delete the group")
        return redirect('/groups')

@login_required
def leave_group(request):

    gateway_id = settings.GATEWAY_ID
    group_id = request.GET.get('group_id')
    user = request.user.username

    try:
        leave = request.sharing_client.removeUsersFromGroup(gateway_id, [user], group_id)
        messages.success(request, 'You are no longer a member of '+group_id+'.')
        return redirect('/groups')
    except Exception as e:
        logger.exception("Failed to leave the group")
        return redirect('/groups')
