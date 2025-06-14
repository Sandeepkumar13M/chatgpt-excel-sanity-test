import pytest
from patchright.sync_api import sync_playwright,TimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

# #-------------------------------------------------------------------------------------------------------------------------

# @pytest.mark.sanity
# def test_sensitive_text():

#     with sync_playwright() as p:
#         # Launch the browser
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()  
#         page.goto("https://m365.cloud.microsoft/")
        
#         # Sign-in sequence
#         page.get_by_role("button", name="Sign in").click()
#         page.wait_for_selector('//*[@id="i0116"]').fill(os.getenv("MS_EMAIL"))
#         page.wait_for_selector('//*[@id="idSIButton9"]').click()
#         page.wait_for_selector('//*[@id="passwordEntry"]').fill(os.getenv("MS_PASSWORD"))
#         page.wait_for_selector('//*[@id="view"]/div/div[5]/button').click()
#         page.wait_for_selector('//*[@id="view"]/div/div[5]/button[2]').click()

#         # Click to open new tab (Excel)
#         page.wait_for_selector('//*[@id="create-new-list"]/div[2]/div[3]/div/div[1]').click()
        
#         page.wait_for_timeout(15000)

#         total_pages = page.context.pages
       
#         new_page = total_pages[1]
#         new_page.bring_to_front()
#         new_page.reload()
        
#         new_page.wait_for_timeout(20000)
#         new_page.screenshot(path="new_tab_screenshot.png")




# Helper to find a button by span text in all frames
def find_button_in_all_frames(page, text):
    for i, frame in enumerate(page.frames):
        try:
            print(f"Searching in frame {i}: {frame.url}")
            button = frame.locator(f'button:has(span:text("{text}"))')
            if button.count() > 0:
                print(f"Found button in frame {i}")
                return button
        except Exception as e:
            print(f"Frame {i} error: {e}")
    return None

@pytest.mark.sanity
def test_sensitive_text():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        new_page = context.new_page()

        # Go to Excel Online file directly
        new_page.goto("https://onedrive.live.com/personal/247443e3fa56e4ce/_layouts/15/doc.aspx?resid=1467f708-9de0-43f7-a858-62952a93a62e&cid=247443e3fa56e4ce&ct=1749924456767&wdOrigin=OFFICECOM-WEB.START.EDGEWORTH&wdPreviousSessionSrc=HarmonyWeb&wdPreviousSession=6b792258-5899-4ec3-878f-83f355dc29e7")

        # Login
        new_page.wait_for_selector('//*[@id="usernameEntry"]').fill(os.getenv("MS_EMAIL"))
        new_page.wait_for_selector('//*[@id="view"]/div/div[3]/button').click()
        new_page.wait_for_selector('//*[@id="passwordEntry"]').fill(os.getenv("MS_PASSWORD"))
        new_page.wait_for_selector('//*[@id="view"]/div/div[5]/button').click()
        new_page.wait_for_selector('//*[@id="view"]/div/div[5]/button[2]').click()

        new_page.wait_for_timeout(15000)
        new_page.pause()  # Remove this in production

        # Handle "Accept" button
        max_retry = 3
        for attempt in range(max_retry):
            try:
                accept_button = new_page.get_by_role("button", name="Accept")
                if accept_button.count() > 0:
                    accept_button.wait_for(state="visible", timeout=5000)
                    accept_button.click()
                    print(f"Attempt {attempt + 1}: Clicked Accept button")
                    break
                else:
                    iframe = new_page.frame_locator("iframe")
                    accept_button = iframe.get_by_role("button", name="Accept")
                    if accept_button.count() > 0:
                        accept_button.wait_for(state="visible", timeout=3000)
                        accept_button.click()
                        print(f"Attempt {attempt + 1}: Clicked Accept button inside iframe")
                        break
                    else:
                        print(f"Attempt {attempt + 1}: Accept button not found")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error: {e}")
                if attempt == max_retry - 1:
                    print("Final failure. HTML snapshot:")
                    print(new_page.content())
                    raise

        new_page.wait_for_load_state("domcontentloaded")
        new_page.reload()
        new_page.reload()
        new_page.wait_for_timeout(15000)

        # Click "Copilot" Ribbon Button
        for attempt in range(max_retry):
            try:
                copilot_button = new_page.locator('button[data-unique-id="Ribbon-Copilot"]')
                if copilot_button.count() > 0:
                    copilot_button.wait_for(state="visible", timeout=5000)
                    copilot_button.click()
                    print(f"Attempt {attempt + 1}: Clicked Copilot button")
                    break
                else:
                    iframe = new_page.frame_locator("iframe")
                    copilot_button = iframe.locator('#Copilot')
                    if copilot_button.count() > 0:
                        copilot_button.wait_for(state="visible", timeout=3000)
                        copilot_button.click()
                        print("Waiting for Copilot panel to load...")
                        new_page.wait_for_timeout(10000)
                        print(f"Attempt {attempt + 1}: Clicked Copilot button inside iframe")
                        break
                    else:
                        print(f"Attempt {attempt + 1}: Copilot button not found")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error: {e}")
                if attempt == max_retry - 1:
                    print("Final failure. HTML snapshot:")
                    print(new_page.content())
                    raise

        new_page.wait_for_timeout(5000)

        #  Now find and click the "Ask Copilot" button in any frame
        for attempt in range(max_retry):
            try:
                button = find_button_in_all_frames(new_page, "Ask Copilot")
                if button:
                    button.wait_for(state="visible", timeout=5000)
                    button.click()
                    print(f"Attempt {attempt + 1}: Clicked 'Ask Copilot' button")
                    break
                else:
                    print(f"Attempt {attempt + 1}: 'Ask Copilot' button not found in any frame")
            except TimeoutError as te:
                print(f"Attempt {attempt + 1}: Timeout clicking Ask Copilot: {te}")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error clicking Ask Copilot: {e}")
                if attempt == max_retry - 1:
                    print("Final HTML Snapshot:\n", new_page.content())
                    raise

        print()
        print(f" New page title: {new_page.title()}")
        new_page.pause()  # For manual inspection (optional)
        browser.close()




        