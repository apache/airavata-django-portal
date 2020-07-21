"""Auth utilities."""

import time
import os
import logging
import json
import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.http.request import split_domain_port
from django.template import Context, Template
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from custos.clients.identity_management_client import IdentityManagementClient
from custos.transport.settings import CustosServerClientSettings

from airavata.model.security.ttypes import AuthzToken

from . import models

from google.protobuf.json_format import MessageToDict

from base64 import b64encode

logger = logging.getLogger(__name__)

custos_settings = CustosServerClientSettings(custos_host=settings.CUSTOS_HOST,
                                             custos_port=settings.CUSTOS_PORT,
                                             custos_client_id=settings.CUSTOS_CLIENT_ID,
                                             custos_client_sec=settings.CUSTOS_CLIENT_SEC,
                                             configuration_file_location=None)

identity_client = IdentityManagementClient(custos_settings)


def get_authz_token(request):
    """Construct AuthzToken instance from session; refresh token if needed."""
    if not is_access_token_expired(request):
        return _create_authz_token(request)
    elif not is_refresh_token_expired(request):
        # Have backend reauthenticate the user with the refresh token
        user = authenticate(request)
        if user:
            return _create_authz_token(request)
    return None


def get_service_account_authz_token():
    portal_token = get_custos_portal_token()
    identity_client = get_custos_identity_client()
    response = identity_client.token(token=portal_token, grant_type='client_credentials')
    token = MessageToDict(response)
    access_token = token.get('access_token')
    custos_id = settings.CUSTOS_CLIENT_ID
    return AuthzToken(
        accessToken=access_token,
        # This is a service account, so leaving out userName for now
        claimsMap={'gatewayID': settings.GATEWAY_ID, 'custosId': custos_id})


def _create_authz_token(request):
    access_token = request.session['ACCESS_TOKEN']
    username = request.user.username
    gateway_id = settings.GATEWAY_ID
    custos_id = settings.CUSTOS_CLIENT_ID
    return AuthzToken(accessToken=access_token,
                      claimsMap={'gatewayID': gateway_id,
                                 'userName': username,
                                 'custosId': custos_id})


def is_access_token_expired(request):
    """Return True if access_token is not available or is expired."""
    now = time.time()
    return not request.user.is_authenticated \
           or 'ACCESS_TOKEN' not in request.session \
           or 'ACCESS_TOKEN_EXPIRES_AT' not in request.session \
           or request.session['ACCESS_TOKEN_EXPIRES_AT'] < now


def is_refresh_token_expired(request):
    """Return True if refresh_token is not available or is expired."""
    now = time.time()
    return 'REFRESH_TOKEN' not in request.session \
           or 'REFRESH_TOKEN_EXPIRES_AT' not in request.session \
           or request.session['REFRESH_TOKEN_EXPIRES_AT'] < now


def send_new_user_email(request, username, email, first_name, last_name):
    """Send new user email notification to portal admins."""
    new_user_email_template = models.EmailTemplate.objects.get(
        pk=models.NEW_USER_EMAIL_TEMPLATE)
    domain, port = split_domain_port(request.get_host())
    context = Context({
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "portal_title": settings.PORTAL_TITLE,
        "gateway_id": settings.GATEWAY_ID,
        "http_host": domain,
    })
    subject = Template(new_user_email_template.subject).render(context)
    body = Template(new_user_email_template.body).render(context)
    msg = EmailMessage(subject=subject,
                       body=body,
                       from_email="{} <{}>".format(
                           settings.PORTAL_TITLE,
                           settings.SERVER_EMAIL),
                       to=[a[1] for a in getattr(settings,
                                                 'PORTAL_ADMINS',
                                                 settings.ADMINS)])
    msg.content_subtype = 'html'
    msg.send()


def send_email_to_user(template_id, context):
    email_template = models.EmailTemplate.objects.get(pk=template_id)
    subject = Template(email_template.subject).render(context)
    body = Template(email_template.body).render(context)
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email="\"{}\" <{}>".format(settings.PORTAL_TITLE,
                                        settings.SERVER_EMAIL),
        to=["\"{} {}\" <{}>".format(context['first_name'],
                                    context['last_name'],
                                    context['email'])],
        reply_to=[f"\"{a[0]}\" <{a[1]}>" for a in getattr(settings,
                                                          'PORTAL_ADMINS',
                                                          settings.ADMINS)]
    )
    msg.content_subtype = 'html'
    msg.send()


def get_custos_authorization_endpoint():
    body = get_custos_openid_config()
    return body['authorization_endpoint']


def get_custos_openid_config():
    encoded_token = get_custos_portal_token()
    response = identity_client.get_oidc_configuration(token=encoded_token, client_id=custos_settings.CUSTOS_CLIENT_ID)
    dict_obj = MessageToDict(response)
    return dict_obj


def get_custos_portal_token():
    decoded_token = settings.CUSTOS_CLIENT_ID + ":" + settings.CUSTOS_CLIENT_SEC
    tokenByte = decoded_token.encode('utf-8')
    encodedBytes = b64encode(tokenByte)
    return encodedBytes.decode('utf-8')


def get_custos_identity_client():
    return identity_client
