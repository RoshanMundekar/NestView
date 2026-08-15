import pytest
from unittest.mock import patch, MagicMock
from NestView.site import is_valid, render_site
from NestView.custom_exception import InvalidURLException


# ─── is_valid() Tests ─────────────────────────────────────────────────────────

class TestIsValid:

    @patch("NestView.site.urllib.request.urlopen")
    def test_valid_url_returns_true(self, mock_urlopen):
        """Should return True when URL responds with HTTP 200."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response

        assert is_valid("https://www.google.com") is True

    @patch("NestView.site.urllib.request.urlopen")
    def test_non_200_status_returns_false(self, mock_urlopen):
        """Should return False when URL responds with a non-200 status code."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 404
        mock_urlopen.return_value = mock_response

        assert is_valid("https://www.example.com/notfound") is False

    @patch("NestView.site.urllib.request.urlopen")
    def test_connection_error_returns_false(self, mock_urlopen):
        """Should return False when a network/connection error occurs."""
        mock_urlopen.side_effect = Exception("Connection refused")
        assert is_valid("https://unreachable.invalid") is False

    @patch("NestView.site.urllib.request.urlopen")
    def test_timeout_returns_false(self, mock_urlopen):
        """Should return False on timeout."""
        mock_urlopen.side_effect = TimeoutError("Timed out")
        assert is_valid("https://slow-site.invalid") is False


# ─── render_site() Tests ──────────────────────────────────────────────────────

class TestRenderSite:

    @patch("NestView.site.display.display")
    @patch("NestView.site.display.IFrame")
    @patch("NestView.site.urllib.request.urlopen")
    def test_valid_url_renders_and_returns_success(self, mock_urlopen, mock_iframe, mock_display):
        """Should render IFrame and return 'success' for a valid URL."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response

        result = render_site("https://www.google.com")
        assert result == "success"
        mock_display.assert_called_once()

    @patch("NestView.site.display.display")
    @patch("NestView.site.display.IFrame")
    @patch("NestView.site.urllib.request.urlopen")
    def test_custom_width_height_passed_to_iframe(self, mock_urlopen, mock_iframe, mock_display):
        """Should pass custom width and height to IFrame."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response

        render_site("https://www.google.com", width="80%", height="900")
        mock_iframe.assert_called_once_with(
            src="https://www.google.com", width="80%", height="900"
        )

    @patch("NestView.site.urllib.request.urlopen")
    def test_invalid_url_raises_exception(self, mock_urlopen):
        """Should raise InvalidURLException for unreachable URLs."""
        mock_urlopen.side_effect = Exception("Could not connect")

        with pytest.raises(InvalidURLException):
            render_site("https://bad-url.invalid")

    @patch("NestView.site.urllib.request.urlopen")
    def test_non_200_response_raises_exception(self, mock_urlopen):
        """Should raise InvalidURLException when response is not 200."""
        mock_response = MagicMock()
        mock_response.getcode.return_value = 403
        mock_urlopen.return_value = mock_response

        with pytest.raises(InvalidURLException):
            render_site("https://www.example.com/forbidden")