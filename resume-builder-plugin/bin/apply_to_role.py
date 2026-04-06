#!/usr/bin/env python3
"""
Semi-automated job application tool using Chrome + Playwright CDP.

Launches system Chrome with remote debugging, then connects via CDP
to automate actions. Chrome stays open between commands so the user
can interact manually (login, CAPTCHAs, complex forms).

Commands:
  launch <url>                Open Chrome and navigate to the job posting
  screenshot                  Capture the current page (returns image path)
  click-apply                 Find and click common Apply buttons
  upload <resume_path>        Upload file to the first file input on page
  click <selector>            Click an element (CSS selector or text=/pattern/)
  fill <selector> <value>     Fill a form field
  select <selector> <value>   Select a dropdown option by visible text
  scroll <direction>          Scroll the page (up/down)
  pages                       List all open tabs
  switch <index>              Switch to a tab by index (from 'pages' output)
  url                         Print current page URL and title
  text                        Extract visible text from current page
  close                       Close the Chrome session and clean up

Examples:
  python3 apply_to_role.py launch "https://linkedin.com/jobs/view/12345"
  python3 apply_to_role.py screenshot
  python3 apply_to_role.py click-apply
  python3 apply_to_role.py upload resume_acme_sre.docx
  python3 apply_to_role.py fill "#firstName" "Bryce"
  python3 apply_to_role.py click "text=Next"
  python3 apply_to_role.py close

Requires: pip3 install playwright
Does NOT require: python3 -m playwright install (uses system Chrome)
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# --- Config ---
STATE_FILE = "/tmp/resume_apply_state.json"
CHROME_PORT = 9222
CHROME_PROFILE = "/tmp/chrome-resume-apply"
SCREENSHOT_PATH = "/tmp/apply_screenshot.png"
CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
]


def _find_chrome():
    """Find the system Chrome executable."""
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    # Try 'which'
    result = subprocess.run(["which", "google-chrome"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    print("Error: Google Chrome not found. Install Chrome or set CHROME_PATH.")
    sys.exit(1)


def _save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def _load_state():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE) as f:
        return json.load(f)


def _connect():
    """Connect to running Chrome via CDP. Returns (pw, browser, page)."""
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    try:
        browser = pw.chromium.connect_over_cdp(f"http://localhost:{CHROME_PORT}")
    except Exception as e:
        pw.stop()
        print(f"Error: Cannot connect to Chrome on port {CHROME_PORT}.")
        print("Run 'launch <url>' first, or check that Chrome is still open.")
        print(f"Details: {e}")
        sys.exit(1)

    pages = browser.contexts[0].pages
    if not pages:
        pw.stop()
        print("Error: No pages open in Chrome.")
        sys.exit(1)

    return pw, browser, pages[-1]


def _disconnect(pw, browser):
    """Disconnect from Chrome without closing it."""
    try:
        browser.close()  # CDP close = disconnect only
    except Exception:
        pass
    try:
        pw.stop()
    except Exception:
        pass


def _screenshot(page, msg="Screenshot saved"):
    """Take a screenshot and print the path."""
    page.screenshot(path=SCREENSHOT_PATH, full_page=False)
    print(f"{msg}: {SCREENSHOT_PATH}")


# --- Commands ---


def cmd_launch(url):
    """Launch Chrome with remote debugging and navigate to URL."""
    # Kill any prior session on the same port
    subprocess.run(
        ["pkill", "-f", f"--remote-debugging-port={CHROME_PORT}"],
        capture_output=True,
    )
    time.sleep(1)

    chrome = _find_chrome()

    proc = subprocess.Popen(
        [
            chrome,
            f"--remote-debugging-port={CHROME_PORT}",
            f"--user-data-dir={CHROME_PROFILE}",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    _save_state({"pid": proc.pid, "url": url, "port": CHROME_PORT})

    # Wait for Chrome to be ready for CDP connections
    for attempt in range(10):
        time.sleep(1)
        try:
            import urllib.request
            urllib.request.urlopen(f"http://localhost:{CHROME_PORT}/json/version", timeout=2)
            break
        except Exception:
            if attempt == 9:
                print(f"Warning: Chrome launched (PID {proc.pid}) but CDP not responding yet.")
                print("Wait a moment and try your next command.")
                return

    print(f"Chrome launched (PID {proc.pid})")
    print(f"Navigated to: {url}")
    print(f"CDP available at: http://localhost:{CHROME_PORT}")

    # Take initial screenshot
    time.sleep(2)
    try:
        pw, browser, page = _connect()
        _screenshot(page, "Initial screenshot")
        _disconnect(pw, browser)
    except Exception:
        print("(Initial screenshot skipped — page may still be loading)")


def cmd_screenshot():
    """Capture the current page."""
    pw, browser, page = _connect()
    try:
        page.wait_for_load_state("domcontentloaded", timeout=5000)
        _screenshot(page)
    finally:
        _disconnect(pw, browser)


def cmd_click_apply():
    """Find and click the Apply button using common selectors."""
    pw, browser, page = _connect()
    try:
        page.wait_for_load_state("networkidle", timeout=10000)

        # Common apply button patterns across job platforms
        selectors = [
            # LinkedIn
            "button.jobs-apply-button",
            "button:has-text('Easy Apply')",
            # Greenhouse
            "#submit_app",
            "a:has-text('Apply for this job')",
            # Lever
            "a.postings-btn",
            # Workday
            "a[data-automation-id='jobApplyButton']",
            # Generic patterns (ordered by specificity)
            "button:has-text('Apply Now')",
            "a:has-text('Apply Now')",
            "button:has-text('Apply for this')",
            "a:has-text('Apply for this')",
            "button:has-text('Apply')",
            "a:has-text('Apply')",
            "[data-automation*='apply']",
            "[class*='apply-button']",
            "[class*='apply_button']",
            "[id*='apply']",
        ]

        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if loc.is_visible(timeout=800):
                    loc.scroll_into_view_if_needed()
                    time.sleep(0.3)
                    loc.click()
                    print(f"Clicked apply button: {sel}")
                    time.sleep(2)
                    page.wait_for_load_state("domcontentloaded", timeout=8000)
                    _screenshot(page, "After clicking apply")
                    return
            except Exception:
                continue

        print("Could not find an apply button automatically.")
        print("Please click it manually in the Chrome window,")
        print("then run 'screenshot' so I can see the next page.")
        _screenshot(page, "Current page state")

    finally:
        _disconnect(pw, browser)


def cmd_upload(resume_path):
    """Upload a file to the first file input found on the page."""
    resume_path = str(Path(resume_path).resolve())
    if not os.path.exists(resume_path):
        print(f"Error: File not found: {resume_path}")
        sys.exit(1)

    pw, browser, page = _connect()
    try:
        page.wait_for_load_state("domcontentloaded", timeout=5000)

        file_inputs = page.locator("input[type='file']")
        count = file_inputs.count()

        if count == 0:
            print("No file upload input found on current page.")
            print("The upload field may appear after clicking a button.")
            _screenshot(page, "Current page (no file input found)")
            return

        if count > 1:
            print(f"Found {count} file inputs. Uploading to the first one.")

        file_inputs.first.set_input_files(resume_path)
        print(f"Uploaded: {resume_path}")
        time.sleep(2)
        _screenshot(page, "After upload")

    finally:
        _disconnect(pw, browser)


def cmd_click(selector):
    """Click an element by CSS selector or text pattern."""
    pw, browser, page = _connect()
    try:
        loc = page.locator(selector).first
        loc.wait_for(state="visible", timeout=5000)
        loc.scroll_into_view_if_needed()
        time.sleep(0.2)
        loc.click()
        print(f"Clicked: {selector}")
        time.sleep(1)
        _screenshot(page, "After click")
    except Exception as e:
        print(f"Error clicking '{selector}': {e}")
        _screenshot(page, "Current page state")
    finally:
        _disconnect(pw, browser)


def cmd_fill(selector, value):
    """Fill a form field by CSS selector."""
    pw, browser, page = _connect()
    try:
        loc = page.locator(selector).first
        loc.wait_for(state="visible", timeout=5000)
        loc.scroll_into_view_if_needed()
        loc.fill(value)
        print(f"Filled '{selector}' with: {value}")
    except Exception as e:
        print(f"Error filling '{selector}': {e}")
        _screenshot(page, "Current page state")
    finally:
        _disconnect(pw, browser)


def cmd_select(selector, value):
    """Select a dropdown option by visible text."""
    pw, browser, page = _connect()
    try:
        loc = page.locator(selector).first
        loc.wait_for(state="visible", timeout=5000)
        loc.select_option(label=value)
        print(f"Selected '{value}' in '{selector}'")
        time.sleep(0.5)
        _screenshot(page, "After selection")
    except Exception as e:
        print(f"Error selecting in '{selector}': {e}")
        _screenshot(page, "Current page state")
    finally:
        _disconnect(pw, browser)


def cmd_scroll(direction="down"):
    """Scroll the page up or down."""
    pw, browser, page = _connect()
    try:
        delta = 600 if direction == "down" else -600
        page.mouse.wheel(0, delta)
        time.sleep(0.5)
        _screenshot(page, f"After scrolling {direction}")
    finally:
        _disconnect(pw, browser)


def cmd_pages():
    """List all open tabs."""
    pw, browser, page = _connect()
    try:
        for ctx in browser.contexts:
            for i, p in enumerate(ctx.pages):
                marker = " <-- active" if p == page else ""
                print(f"  [{i}] {p.title()} — {p.url}{marker}")
    finally:
        _disconnect(pw, browser)


def cmd_switch(index):
    """Bring a tab to focus by index."""
    pw, browser, page = _connect()
    try:
        pages = browser.contexts[0].pages
        idx = int(index)
        if 0 <= idx < len(pages):
            pages[idx].bring_to_front()
            print(f"Switched to tab [{idx}]: {pages[idx].title()}")
            time.sleep(0.5)
            _screenshot(pages[idx], "Active tab")
        else:
            print(f"Error: Index {idx} out of range. Use 'pages' to see available tabs.")
    finally:
        _disconnect(pw, browser)


def cmd_url():
    """Print current page URL and title."""
    pw, browser, page = _connect()
    try:
        print(f"Title: {page.title()}")
        print(f"URL:   {page.url}")
    finally:
        _disconnect(pw, browser)


def cmd_text():
    """Extract visible text from current page (for Claude to read without screenshot)."""
    pw, browser, page = _connect()
    try:
        text = page.inner_text("body")
        # Collapse whitespace but preserve structure
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        output = "\n".join(lines)
        # Cap at reasonable length
        if len(output) > 8000:
            output = output[:8000] + "\n... (truncated)"
        print(output)
    finally:
        _disconnect(pw, browser)


def cmd_close():
    """Close the Chrome session and clean up temp files."""
    state = _load_state()
    if state and state.get("pid"):
        subprocess.run(["kill", str(state["pid"])], capture_output=True)
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    subprocess.run(["rm", "-rf", CHROME_PROFILE], capture_output=True)
    if os.path.exists(SCREENSHOT_PATH):
        os.remove(SCREENSHOT_PATH)
    print("Chrome session closed and temp files cleaned up.")


# --- CLI ---

COMMANDS = {
    "launch":      (cmd_launch,      1, "<url>"),
    "screenshot":  (cmd_screenshot,  0, ""),
    "click-apply": (cmd_click_apply, 0, ""),
    "upload":      (cmd_upload,      1, "<resume_path>"),
    "click":       (cmd_click,       1, "<selector>"),
    "fill":        (cmd_fill,        2, "<selector> <value>"),
    "select":      (cmd_select,      2, "<selector> <value>"),
    "scroll":      (cmd_scroll,      0, "[up|down]"),
    "pages":       (cmd_pages,       0, ""),
    "switch":      (cmd_switch,      1, "<tab_index>"),
    "url":         (cmd_url,         0, ""),
    "text":        (cmd_text,        0, ""),
    "close":       (cmd_close,       0, ""),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: python3 apply_to_role.py <command> [args]\n")
        print("Commands:")
        for name, (_, _, usage) in COMMANDS.items():
            print(f"  {name:14s} {usage}")
        print("\nRequires: pip3 install playwright")
        sys.exit(0 if len(sys.argv) < 2 else 1)

    cmd_name = sys.argv[1]
    func, min_args, usage = COMMANDS[cmd_name]
    args = sys.argv[2:]

    if len(args) < min_args:
        print(f"Usage: python3 apply_to_role.py {cmd_name} {usage}")
        sys.exit(1)

    func(*args[:max(min_args, len(args))])


if __name__ == "__main__":
    main()
