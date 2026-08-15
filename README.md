# NestView 🚀

[![PyPI version](https://img.shields.io/pypi/v/NestView.svg)](https://pypi.org/project/NestView/)
[![Python versions](https://img.shields.io/pypi/pyversions/NestView.svg)](https://pypi.org/project/NestView/)
[![License](https://img.shields.io/pypi/l/NestView.svg)](https://github.com/roshanmundekar/NestView/blob/main/LICENSE)
[![Tests](https://github.com/roshanmundekar/NestView/actions/workflows/python-publish.yml/badge.svg)](https://github.com/roshanmundekar/NestView/actions)

---

**NestView** is a lightweight Python library designed for **Data Scientists** and **Jupyter Notebook** users.  
It lets you seamlessly render live websites and embed YouTube videos **directly inside** your `.ipynb` environment — no more switching tabs!

Works with **Jupyter Notebook**, **JupyterLab**, and **Google Colab**.

---

## ✨ Features

- 🌐 **Website Rendering** — Render any HTTPS website directly inside a Jupyter output cell via `IFrame`.
- ▶️ **YouTube Integration** — Intelligent regex parsing of YouTube URLs (standard, short, embed, playlist) to extract video ID and embed the player automatically.
- 📏 **Customizable Dimensions** — Easily adjust `width` and `height` of the rendered viewport.
- 🛡️ **Custom Exceptions** — Clean `InvalidURLException` for clear error messages on bad or non-YouTube URLs.
- 📋 **Built-in Logging** — Structured logging to both console and file (`logs/running_logs.log`).
- 🧪 **Fully Tested** — 22 unit + integration tests with `pytest` and `unittest.mock`.
- 🖥️ **Browser Demo** — Standalone `demo_browser.py` script to visually verify rendering without Jupyter.
- ⚡ **Lightweight** — Built on top of standard IPython display tools with minimal dependencies.

---

## 📦 Installation

```bash
pip install NestView
```

---

## 🚀 Quick Start

### ▶️ Embed a YouTube Video

```python
from NestView.youtube import render_youtube_video

# Standard URL
render_youtube_video("https://www.youtube.com/watch?v=xOK2SRzmmQw")

# Short URL
render_youtube_video("https://youtu.be/xOK2SRzmmQw")

# Playlist URL (video ID still extracted correctly)
render_youtube_video("https://www.youtube.com/watch?v=xOK2SRzmmQw&list=PL123&index=3")

# Custom size
render_youtube_video("https://www.youtube.com/watch?v=xOK2SRzmmQw", width=1200, height=675)
```

### 🌐 Render a Website

```python
from NestView.site import render_site

render_site("https://www.python.org")

# Custom dimensions
render_site("https://docs.python.org", width="100%", height="800")
```

---

## 📁 Project Structure

```
NestView/
├── src/
│   └── NestView/
│       ├── __init__.py           # Package init
│       ├── custom_exception.py   # InvalidURLException
│       ├── logger.py             # Logging setup (file + console)
│       ├── site.py               # render_site() — IFrame website renderer
│       └── youtube.py            # render_youtube_video() — YouTube embed
├── tests/
│   ├── unit/
│   │   └── test_unit.py          # 14 unit tests (exception + YouTube)
│   └── integration/
│       └── test_int.py           # 8 integration tests (site validation)
├── logs/
│   └── running_logs.log          # Auto-generated log file
├── demo_browser.py               # Standalone browser demo (no Jupyter needed)
├── setup.py
├── setup.cfg
├── pyproject.toml
├── tox.ini
├── requirements.txt
└── requirements_dev.txt
```

---

## 🛠️ Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/roshanmundekar/NestView.git
cd NestView
```

### 2. Create and activate a virtual environment

```bash
conda create -n nestview_env python=3.8 -y
conda activate nestview_env
```

### 3. Install in editable mode with dev dependencies

```bash
pip install -r requirements_dev.txt
```

> The `-e .` in `requirements_dev.txt` installs the package in editable mode so source changes reflect immediately.

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

---

## 🖥️ Browser Demo (No Jupyter Needed)

NestView includes a standalone demo script that opens a visual proof page in your browser.  
It shows all three capabilities: YouTube embed, website render, and error handling.

```bash
# Run with default URLs
python demo_browser.py

# Custom YouTube video
python demo_browser.py --youtube "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

# Custom website
python demo_browser.py --site "https://yourwebsite.com"

# All options together
python demo_browser.py --youtube "URL" --site "URL" --bad "URL"

# Show all options
python demo_browser.py --help
```

> **Tip:** Before using a YouTube URL, verify it allows embedding:  
> `https://www.youtube.com/oembed?url=YOUR_URL&format=json`  
> Returns **200** → embeddable. Returns **401** → embedding disabled by owner.

---

## 🧪 Running Tests

```bash
# Run all 22 tests
pytest -v tests/

# Run only unit tests
pytest -v tests/unit

# Run only integration tests
pytest -v tests/integration
```

Expected output:
```
22 passed in 1.32s
```

### Using Tox (runs flake8 + mypy + pytest across Python 3.8 & 3.9)

```bash
tox
```

---

## 📖 API Reference

### `render_youtube_video(url, width=780, height=440)`

Parses a YouTube URL using regex, extracts the 11-character video ID, and embeds the player inside the Jupyter output cell using a privacy-friendly `youtube-nocookie.com` embed.

| Parameter | Type  | Default | Description                    |
|-----------|-------|---------|--------------------------------|
| `url`     | `str` | —       | YouTube video URL (any format) |
| `width`   | `int` | `780`   | Width of the embedded player   |
| `height`  | `int` | `440`   | Height of the embedded player  |

**Supported URL formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&list=...&index=...`

**Raises:** `InvalidURLException` if no valid YouTube video ID is found.  
**Returns:** `"success"` on successful render.

---

### `render_site(url, width="100%", height="600")`

Validates and renders a live website inside a Jupyter output cell using an `IFrame`.

| Parameter | Type  | Default   | Description                    |
|-----------|-------|-----------|--------------------------------|
| `url`     | `str` | —         | Full HTTPS URL of the website  |
| `width`   | `str` | `"100%"`  | Width of the iframe            |
| `height`  | `str` | `"600"`   | Height of the iframe           |

**Raises:** `InvalidURLException` if the URL is unreachable or returns a non-200 status.  
**Returns:** `"success"` on successful render.

---

### `InvalidURLException`

Custom exception raised when a URL is invalid, unreachable, or not a valid YouTube link.

```python
from NestView.custom_exception import InvalidURLException

# Custom message
raise InvalidURLException("Bad link provided")

# Default message: "The provided URL is invalid."
raise InvalidURLException()
```

---

## 🔧 Logging

NestView uses a built-in logger that writes to both the console and `logs/running_logs.log`.

**Log format:**
```
[YYYY-MM-DD HH:MM:SS,ms: LEVEL: module]: message
```

**Example output:**
```
[2026-08-15 23:20:24,812: INFO: demo_browser]: Building NestView demo page...
[2026-08-15 23:20:24,906: ERROR: demo_browser]: Expected error caught: Invalid YouTube URL
```

**Use the logger in your own code:**
```python
from NestView.logger import logger

logger.info("Your message here")
logger.error("Something went wrong")
```

---

## 📋 Requirements

**Runtime:**
```
ipython
py-youtube==1.1.7
ensure==1.0.2
```

**Development:**
```
pytest==7.1.3
tox==3.25.1
flake8==5.0.4
mypy==0.971
mkdocs-material
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and add tests
4. Run `pytest -v tests/` to ensure all tests pass
5. Run `tox` for full lint + type + test checks
6. Submit a pull request

---

## 📄 License

This project is licensed under the **Apache License 2.0**.  
See the [LICENSE](https://github.com/roshanmundekar/NestView/blob/main/LICENSE) file for details.

---

## 👤 Author

**Roshan Mundekar**  
GitHub: [@roshanmundekar](https://github.com/roshanmundekar)  
PyPI: [NestView](https://pypi.org/project/NestView/)
