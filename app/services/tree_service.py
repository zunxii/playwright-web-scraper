import time
from app.config import GLOBAL_TIMEOUT, CLICK_TIMEOUT
from app.utils.dom_parser import BUILD_TREE_JS
from app.services.playwright_utils import get_browser

TOGGLE_SELECTORS = [
    "ul#myUL span.caret:not(.caret-down)",
    ".ui-treenode-toggler.ui-icon, .ui-treenode-icon.ui-icon",
    "[aria-expanded='false']",
    ".caret:not(.caret-down)",
    ".toggle:not(.open)",
]

def expand_all_toggles(page, timeout_s=GLOBAL_TIMEOUT):
    start = time.time()
    total_clicked = 0

    while True:
        if time.time() - start > timeout_s:
            break

        progress = False
        for sel in TOGGLE_SELECTORS:
            elements = page.query_selector_all(sel) or []
            for el in elements:
                try:
                    if not el.is_visible():
                        continue
                    el.scroll_into_view_if_needed()
                    try:
                        el.click(timeout=CLICK_TIMEOUT)
                    except Exception:
                        el.evaluate("el => el.click()")
                    total_clicked += 1
                    progress = True
                    page.wait_for_timeout(150)
                except Exception:
                    continue
            if progress:
                break
        if not progress:
            break

    return total_clicked


def scrape_tree(url: str):
    p, browser = get_browser()
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)

    clicked = expand_all_toggles(page)
    tree = page.evaluate(BUILD_TREE_JS)

    browser.close()
    p.stop()

    return {"url": url, "clicked": clicked, "tree": tree}
