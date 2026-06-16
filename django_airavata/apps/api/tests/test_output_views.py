from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from django_airavata import middleware
from django_airavata.apps.api import output_views


class HtmlFileViewProviderTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_html_file_provider_is_registered_as_default_provider(self):
        self.assertIn("html-file", output_views.DEFAULT_VIEW_PROVIDERS)
        self.assertEqual(
            "html-iframe",
            output_views.DEFAULT_VIEW_PROVIDERS["html-file"].display_type)

    def test_html_file_provider_returns_html_download_url(self):
        request = self.factory.get("/")
        experiment_output = SimpleNamespace(
            value="airavata-dp://test-gateway/html-report")

        view_data = output_views.DEFAULT_VIEW_PROVIDERS[
            "html-file"].generate_data(
                request,
                experiment_output,
                experiment=SimpleNamespace())

        parsed_url = urlparse(view_data["url"])
        query_params = parse_qs(parsed_url.query)
        self.assertEqual("/sdk/download/", parsed_url.path)
        self.assertEqual(
            ["airavata-dp://test-gateway/html-report"],
            query_params["data-product-uri"])
        self.assertEqual(["text/html"], query_params["mime-type"])


class HtmlOutputFrameOptionsMiddlewareTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def _response_with_deny_frame_options(self, request):
        response = HttpResponse()
        response["X-Frame-Options"] = "DENY"
        return response

    def test_html_download_file_responses_can_be_framed_same_origin(self):
        request = self.factory.get(
            "/sdk/download-file/",
            {"mime-type": "text/html"})

        response = middleware.HtmlOutputFrameOptionsMiddleware(
            self._response_with_deny_frame_options)(request)

        self.assertEqual("SAMEORIGIN", response["X-Frame-Options"])
        self.assertEqual("sandbox", response["Content-Security-Policy"])

    def test_non_html_download_file_responses_keep_existing_frame_options(self):
        request = self.factory.get(
            "/sdk/download-file/",
            {"mime-type": "text/plain"})

        response = middleware.HtmlOutputFrameOptionsMiddleware(
            self._response_with_deny_frame_options)(request)

        self.assertEqual("DENY", response["X-Frame-Options"])
        self.assertNotIn("Content-Security-Policy", response)

    def test_html_output_frame_options_middleware_is_installed(self):
        self.assertIn(
            "django_airavata.middleware.HtmlOutputFrameOptionsMiddleware",
            settings.MIDDLEWARE)
