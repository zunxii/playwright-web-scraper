from playwright.sync_api import sync_playwright
from app import config

def get_browser():
    """Launch a Playwright browser instance with safe defaults (works in Docker + local)."""
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=config.HEADLESS,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    )
    return p, browser
