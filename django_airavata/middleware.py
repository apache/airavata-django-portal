
import logging

import thrift
import thrift.transport.TTransport
from django.shortcuts import render

from . import utils

logger = logging.getLogger(__name__)


class HtmlOutputFrameOptionsMiddleware:
    """Apply browser protections for HTML output downloads."""

    CSP_HEADER = "Content-Security-Policy"
    HTML_OUTPUT_DOWNLOAD_PATHS = {
        "/sdk/download/",
        "/sdk/download-file/",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        mime_type = request.GET.get("mime-type", "").split(";", 1)[0].strip().lower()
        if (request.path in self.HTML_OUTPUT_DOWNLOAD_PATHS and
                mime_type == "text/html"):
            response["X-Frame-Options"] = "SAMEORIGIN"
            response[self.CSP_HEADER] = self._with_strict_sandbox_csp(
                response.get(self.CSP_HEADER, ""))
        return response

    def _with_strict_sandbox_csp(self, csp):
        directives = []
        for directive in csp.split(";"):
            directive = directive.strip()
            if not directive:
                continue
            directive_name = directive.split(None, 1)[0].lower()
            if directive_name != "sandbox":
                directives.append(directive)
        directives.append("sandbox")
        return "; ".join(directives)


class AiravataClientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with utils.airavata_api_client_pool.connection() as airavata_client:
            request.airavata_client = airavata_client
            response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, thrift.transport.TTransport.TTransportException):
            return render(
                request,
                'django_airavata/error_page.html',
                status=500,
                context={
                    'title': 'Airavata is down',
                    'text': """The Airavata API server is not reachable. Please try again."""})
        else:
            return None


def profile_service_client(get_response):
    """Open and close Profile Service client for each request.

    Usage:
        request.profile_service['group_manager'].getGroup(
            request.authz_token, groupId)
    """
    def middleware(request):

        request.profile_service = {
            'group_manager': utils.group_manager_client_pool,
            'iam_admin': utils.iamadmin_client_pool,
            'tenant_profile': utils.tenant_profile_client_pool,
            'user_profile': utils.user_profile_client_pool,
        }
        response = get_response(request)

        return response

    return middleware
