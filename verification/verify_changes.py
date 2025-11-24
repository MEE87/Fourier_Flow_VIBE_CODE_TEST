from playwright.sync_api import sync_playwright, expect
import time

def verify_studio_controls(page):
    print("Navigating to Home...")
    page.goto("http://localhost:8080/index.html")
    time.sleep(1) # wait for fade in

    print("Navigating to Studio...")
    page.click("#nav-studio")
    time.sleep(1) # wait for transition

    # Check if Studio controls panel exists
    panel = page.locator("#studio-controls-panel")
    expect(panel).to_be_visible()

    # Check text inside
    expect(panel).to_contain_text("TOOLS")
    expect(panel).to_contain_text("VIBE MODE")

    # Simulate a drawing
    canvas = page.locator("#canvas-draw")
    box = canvas.bounding_box()

    print("Drawing on canvas...")
    page.mouse.move(box["x"] + 100, box["y"] + 100)
    page.mouse.down()
    page.mouse.move(box["x"] + 200, box["y"] + 100) # Line
    page.mouse.move(box["x"] + 200, box["y"] + 200) # Square-ish
    page.mouse.move(box["x"] + 100, box["y"] + 200)
    page.mouse.move(box["x"] + 100, box["y"] + 100)
    page.mouse.up()

    # Wait for FFT calculation (it might be instant or show loading)
    # The loading overlay might appear briefly.
    time.sleep(1)

    # Check status message
    status = page.locator("#status-msg")
    # It should say "Drawing (X cycles)"
    text = status.text_content()
    print(f"Status: {text}")
    assert "Drawing" in text

    # Take screenshot of Desktop view
    page.screenshot(path="verification/studio_desktop.png")
    print("Desktop screenshot saved.")

def verify_mobile_view(page):
    print("Switching to Mobile Viewport...")
    page.set_viewport_size({"width": 375, "height": 667})
    page.reload()
    time.sleep(1)

    page.click("#nav-studio")
    time.sleep(1)

    # Check if panel is positioned at bottom (we can check CSS or visual)
    panel = page.locator("#studio-controls-panel")
    expect(panel).to_be_visible()

    # Take screenshot
    page.screenshot(path="verification/studio_mobile.png")
    print("Mobile screenshot saved.")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    try:
        verify_studio_controls(page)
        verify_mobile_view(page)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.close()
