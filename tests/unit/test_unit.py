import pytest
from unittest.mock import patch, MagicMock
from NestView.custom_exception import InvalidURLException
from NestView.youtube import render_youtube_video


# ─── InvalidURLException Tests ────────────────────────────────────────────────

class TestInvalidURLException:

    def test_default_message(self):
        """Exception should use default message when none is provided."""
        exc = InvalidURLException()
        assert str(exc) == "The provided URL is invalid."

    def test_custom_message(self):
        """Exception should use the custom message when provided."""
        exc = InvalidURLException("Bad link!")
        assert str(exc) == "Bad link!"

    def test_is_exception_subclass(self):
        """InvalidURLException must be a subclass of Exception."""
        assert issubclass(InvalidURLException, Exception)

    def test_can_be_raised_and_caught(self):
        """Should be raise-able and catchable like any standard exception."""
        with pytest.raises(InvalidURLException):
            raise InvalidURLException()


# ─── render_youtube_video Tests ───────────────────────────────────────────────

class TestRenderYoutubeVideo:

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_standard_url(self, mock_html, mock_display):
        """Should successfully render a standard YouTube watch URL."""
        result = render_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert result == "success"
        mock_display.assert_called_once()

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_short_url(self, mock_html, mock_display):
        """Should successfully parse a youtu.be short URL."""
        result = render_youtube_video("https://youtu.be/dQw4w9WgXcQ")
        assert result == "success"
        mock_display.assert_called_once()

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_url_with_timestamp(self, mock_html, mock_display):
        """Should handle YouTube URLs that include a timestamp parameter."""
        result = render_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s")
        assert result == "success"

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_embed_url(self, mock_html, mock_display):
        """Should handle YouTube embed-format URLs."""
        result = render_youtube_video("https://www.youtube.com/embed/dQw4w9WgXcQ")
        assert result == "success"

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_custom_dimensions(self, mock_html, mock_display):
        """Should pass custom width and height into the iframe HTML."""
        render_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", width=1200, height=675)
        html_content = mock_html.call_args[0][0]
        assert '1200' in html_content
        assert '675' in html_content

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_embed_uses_nocookie_domain(self, mock_html, mock_display):
        """Embed URL should use youtube-nocookie.com for privacy."""
        render_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        html_content = mock_html.call_args[0][0]
        assert "youtube-nocookie.com" in html_content

    @patch("NestView.youtube.display")
    @patch("NestView.youtube.HTML")
    def test_correct_video_id_extracted(self, mock_html, mock_display):
        """The correct 11-char video ID must appear in the embed URL."""
        render_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        html_content = mock_html.call_args[0][0]
        assert "dQw4w9WgXcQ" in html_content

    def test_invalid_url_raises_exception(self):
        """A non-YouTube URL should raise InvalidURLException."""
        with pytest.raises(InvalidURLException):
            render_youtube_video("https://www.google.com")

    def test_empty_string_raises_exception(self):
        """An empty string URL should raise InvalidURLException."""
        with pytest.raises(InvalidURLException):
            render_youtube_video("")

    def test_random_string_raises_exception(self):
        """A random string should raise InvalidURLException."""
        with pytest.raises(InvalidURLException):
            render_youtube_video("not_a_url_at_all")