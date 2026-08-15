"""
NestView - Live Browser Demo
=============================
Run this script to visually verify that NestView can:
  1. Embed a YouTube video (rendered as iframe in browser)
  2. Render a website (rendered as iframe in browser)

Usage:
    # Run with defaults
    python demo_browser.py

    # Pass custom URLs via CLI
    python demo_browser.py --youtube "https://www.youtube.com/watch?v=YOUR_ID"
    python demo_browser.py --site "https://yoursite.com"
    python demo_browser.py --youtube "URL" --site "URL" --bad "URL"
"""

import os
import re
import webbrowser
import tempfile
import argparse

from NestView.custom_exception import InvalidURLException
from NestView.logger import logger


# ─── YouTube URL Parser (same logic as youtube.py) ────────────────────────────

def build_youtube_embed(url: str, width: int = 780, height: int = 440) -> str:
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if not match:
        raise InvalidURLException(f"Invalid YouTube URL: {url}")
    video_id = match.group(1)
    embed_url = f"https://www.youtube-nocookie.com/embed/{video_id}"
    return f"""
    <div class="card">
        <h2>▶️ YouTube Video</h2>
        <p class="url">URL: <code>{url}</code></p>
        <p class="status ok">✅ Valid YouTube URL detected — Video ID: <strong>{video_id}</strong></p>
        <p class="note">⚠️ Note: Some videos disable embedding by owner — if blank, try a different URL.</p>
        <div class="embed-wrap">
            <iframe width="{width}" height="{height}"
                src="{embed_url}"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen>
                <p style="color:#f87171;padding:20px">This video cannot be embedded (embedding disabled by owner).</p>
            </iframe>
        </div>
    </div>
    """


def build_site_embed(url: str, width: str = "100%", height: str = "500") -> str:
    import urllib.request
    import ssl
    ctx = ssl._create_unverified_context()  # bypass SSL cert check for demo connectivity test
    try:
        code = urllib.request.urlopen(url, context=ctx).getcode()
        status_html = f'<p class="status ok">HTTP {code} - Site is reachable</p>'
    except Exception as e:
        status_html = f'<p class="status fail">Could not reach site: {e}</p>'
        return f"""
        <div class="card">
            <h2>Website Rendering</h2>
            <p class="url">URL: <code>{url}</code></p>
            {status_html}
        </div>
        """

    return f"""
    <div class="card">
        <h2>🌐 Website Rendering</h2>
        <p class="url">URL: <code>{url}</code></p>
        {status_html}
        <div class="embed-wrap">
            <iframe width="{width}" height="{height}"
                src="{url}"
                frameborder="0">
            </iframe>
        </div>
    </div>
    """


def build_invalid_demo(url: str) -> str:
    try:
        build_youtube_embed(url)
        return ""
    except InvalidURLException as e:
        logger.error(f"Expected error caught: {e}")
        return f"""
        <div class="card error-card">
            <h2>🛡️ Error Handling Demo</h2>
            <p class="url">URL: <code>{url}</code></p>
            <p class="status fail">❌ InvalidURLException raised — <strong>{e}</strong></p>
            <p class="note">This is correct behaviour! NestView correctly rejects invalid URLs.</p>
        </div>
        """


# ─── HTML Page Builder ─────────────────────────────────────────────────────────

def build_html_page(youtube_url: str, site_url: str, bad_url: str) -> str:
    youtube_block  = build_youtube_embed(youtube_url)
    site_block     = build_site_embed(site_url)
    invalid_block  = build_invalid_demo(bad_url)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NestView — Live Demo</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #0f1117;
            color: #e2e8f0;
            padding: 40px 20px;
        }}
        header {{
            text-align: center;
            margin-bottom: 48px;
        }}
        header h1 {{
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6ee7f7, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        header p {{
            color: #94a3b8;
            font-size: 1.05rem;
        }}
        .badge {{
            display: inline-block;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.8rem;
            color: #7dd3fc;
            margin: 6px 4px 0;
        }}
        .card {{
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 28px 32px;
            margin: 0 auto 32px;
            max-width: 900px;
        }}
        .error-card {{
            border-color: #ef4444;
            background: #1a0a0a;
        }}
        .card h2 {{
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #f1f5f9;
        }}
        .url {{ margin-bottom: 8px; color: #94a3b8; font-size: 0.9rem; }}
        .url code {{
            background: #0f172a;
            padding: 2px 8px;
            border-radius: 6px;
            color: #7dd3fc;
        }}
        .status {{ margin-bottom: 16px; font-weight: 600; }}
        .ok    {{ color: #4ade80; }}
        .fail  {{ color: #f87171; }}
        .note  {{ color: #94a3b8; font-size: 0.9rem; margin-top: 8px; }}
        .embed-wrap {{
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #334155;
            margin-top: 8px;
        }}
        .embed-wrap iframe {{ display: block; width: 100%; }}
        footer {{
            text-align: center;
            color: #475569;
            font-size: 0.85rem;
            margin-top: 20px;
        }}
        footer strong {{ color: #7dd3fc; }}
    </style>
</head>
<body>
    <header>
        <h1>🚀 NestView</h1>
        <p>Live Demo — verifying that rendering works correctly</p>
        <span class="badge">👤 Roshan Mundekar</span>
        <span class="badge">🐍 Python Library</span>
        <span class="badge">📓 Jupyter Ready</span>
    </header>

    {youtube_block}
    {site_block}
    {invalid_block}

    <footer>
        <p>Built with ❤️ by <strong>Roshan Mundekar</strong> · NestView Library Demo</p>
    </footer>
</body>
</html>"""


# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NestView Live Browser Demo — renders YouTube and websites in browser"
    )
    parser.add_argument(
        "--youtube",
        default="https://www.youtube.com/watch?v=xOK2SRzmmQw",
        help="YouTube video URL to embed (default: FxGLvMHY29o)"
    )
    parser.add_argument(
        "--site",
        default="https://httpbin.org",
        help="Website URL to render in iframe (default: httpbin.org)"
    )
    parser.add_argument(
        "--bad",
        default="https://www.google.com/maps/@19.1710901,73.004356,6581m/data=!3m1!1e3!5m1!1e1?entry=ttu&g_ep=EgoyMDI2MDgxMi4wIKXMDSoASAFQAw%3D%3D",
        help="Non-YouTube URL to demo InvalidURLException (default: google.com/maps)"
    )
    args = parser.parse_args()

    YOUTUBE_URL = args.youtube
    SITE_URL    = args.site
    BAD_URL     = args.bad

    logger.info(f"YouTube URL : {YOUTUBE_URL}")
    logger.info(f"Site URL    : {SITE_URL}")
    logger.info(f"Bad URL     : {BAD_URL}")
    logger.info("Building NestView demo page...")

    html = build_html_page(YOUTUBE_URL, SITE_URL, BAD_URL)

    # Write to a temp HTML file and open in browser
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html",
                                     delete=False, encoding="utf-8")
    tmp.write(html)
    tmp.close()

    logger.info(f"Opening demo in browser: {tmp.name}")
    webbrowser.open(f"file:///{tmp.name}")
    print(f"\nDemo opened in browser: {tmp.name}\n")
