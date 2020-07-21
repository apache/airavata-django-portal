"""Django Airavata Auth Backends: KeycloakBackend."""
import logging
import time

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_variables
from oauthlib.oauth2 import InvalidGrantError, LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from google.protobuf.json_format import MessageToDict

from . import utils

from google.auth import jwt

logger = logging.getLogger(__name__)


class KeycloakBackend(object):
    """Django authentication backend for Keycloak."""

    # mask all local variables from error emails since they contain the user's
    # password and/or client_secret. Note, we could selectively just hide
    # variables that are sensitive, but this decorator doesn't apply explicitly
    # listed variable masking to library function calls
    @sensitive_variables()
    def authenticate(self,
                     request=None,
                     username=None,
                     password=None,
                     refresh_token=None):
        try:
            if username and password:
                token, userinfo = self._get_token_and_userinfo_password_flow(
                    username, password)
                if token is None:  # login failed
                    return None
                self._process_token(request, token)
                return self._process_userinfo(request, userinfo)
            # user is already logged in and can use refresh token
            elif request.user and not utils.is_refresh_token_expired(request):
                logger.debug("Refreshing token...")
                token, userinfo = \
                    self._get_token_and_userinfo_from_refresh_token(request)
                self._process_token(request, token)
                # user is already logged in
                return request.user
            elif refresh_token:
                logger.debug("Refreshing supplied token...")
                token, userinfo = \
                    self._get_token_and_userinfo_from_refresh_token(
                        request, refresh_token=refresh_token)
                self._process_token(request, token)
                return self._process_userinfo(request, userinfo)
            else:
                token, userinfo = self._get_token_and_userinfo_redirect_flow(
                    request)
                self._process_token(request, token)
                return self._process_userinfo(request, userinfo)
        except Exception as e:
            logger.exception("login failed")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _get_token_and_userinfo_password_flow(self, username, password):
        try:
            identity_client = utils.get_custos_identity_client()
            portal_token = utils.get_custos_portal_token()

            response = identity_client.token(token=portal_token, username=username,
                                             password=password,
                                             grant_type='password')
            token = MessageToDict(response)

            logger.info(token)
            # refresh_token doesn't take client_secret kwarg, so create auth
            # explicitly
            userinfo = self._get_userinfo_from_token(token["access_token"])

            return token, userinfo
        except InvalidGrantError as e:
            # password wasn't valid, just log as a warning
            logger.warning(f"Failed to log in user {username} with "
                           f"password: {e}")
            return None, None

    def _get_token_and_userinfo_redirect_flow(self, request):
        identity_client = utils.get_custos_identity_client()
        portal_token = utils.get_custos_portal_token()

        code = request.GET.get('code')
        state = request.GET.get('state')
        session_state = request.GET.get('session_state')

        saved_state = request.session['OAUTH2_STATE']
        redirect_uri = request.session['OAUTH2_REDIRECT_URI']

        logger.debug("Code: {}, State: {}, Saved_state: {}, session_state: {}".format(code, state, saved_state,
                                                                                      session_state))
        if state == saved_state:
            response = identity_client.token(token=portal_token, redirect_uri=redirect_uri, code=code)
            token = MessageToDict(response)

            userinfo = self._get_userinfo_from_token(token["access_token"])

            return token, userinfo
        else:
            logger.exception("Token mismatch error")
            return None

    def _get_token_and_userinfo_from_refresh_token(self,
                                                   request,
                                                   refresh_token=None):
        refresh_token_ = (refresh_token
                          if refresh_token is not None
                          else request.session['REFRESH_TOKEN'])
        identity_client = utils.get_custos_identity_client()
        portal_token = utils.get_custos_portal_token()

        response = identity_client.token(token=portal_token, refresh_token=refresh_token_, grant_type='refresh_token')
        token = MessageToDict(response)

        # refresh_token doesn't take client_secret kwarg, so create auth
        # explicitly
        userinfo = self._get_userinfo_from_token(token["access_token"])

        return token, userinfo

    def _process_token(self, request, token):
        # TODO validate the JWS signature
        now = time.time()
        # Put access_token into session to be used for authenticating with API
        # server
        sess = request.session
        sess['ACCESS_TOKEN'] = token['access_token']
        sess['ACCESS_TOKEN_EXPIRES_AT'] = now + token['expires_in']
        sess['REFRESH_TOKEN'] = token['refresh_token']
        sess['REFRESH_TOKEN_EXPIRES_AT'] = now + token['refresh_expires_in']

    def _process_userinfo(self, request, userinfo):
        logger.debug("userinfo: {}".format(userinfo))
        username = userinfo['preferred_username']
        email = userinfo['email']
        first_name = userinfo['given_name']
        last_name = userinfo['family_name']
        request.session['USERINFO'] = userinfo
        try:
            user = User.objects.get(username=username)
            # Update these fields each time, in case they have changed
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return user
        except User.DoesNotExist:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email)
            user.save()
            utils.send_new_user_email(
                request, username, email, first_name, last_name)
            return user

    def _get_userinfo_from_token(self, token):
        userinfo = {}
        decoded_id_token = jwt.decode(token, verify=False)
        userinfo["preferred_username"] = decoded_id_token["preferred_username"]
        userinfo["given_name"] = decoded_id_token["given_name"]
        userinfo["family_name"] = decoded_id_token["family_name"]
        userinfo["email"] = decoded_id_token["email"]
        return userinfo
