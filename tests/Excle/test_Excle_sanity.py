import pytest
from patchright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.sanity
def test_sensitive_text():

    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()  
        page.goto("https://m365.cloud.microsoft/")
        
        # Sign-in sequence
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_selector('//*[@id="i0116"]').fill(os.getenv("MS_EMAIL"))
        page.wait_for_selector('//*[@id="idSIButton9"]').click()
        page.wait_for_selector('//*[@id="passwordEntry"]').fill(os.getenv("MS_PASSWORD"))
        page.wait_for_selector('//*[@id="view"]/div/div[5]/button').click()
        page.wait_for_selector('//*[@id="view"]/div/div[5]/button[2]').click()

        # Click to open new tab (Excel)
        page.wait_for_selector('//*[@id="create-new-list"]/div[2]/div[3]/div/div[1]').click()
        
        page.wait_for_timeout(15000)

        total_pages = page.context.pages
        # print(f"Total pages: {len(total_pages)}")
        # for i, p in enumerate(total_pages):
        #     print(f"Page {i}: {p.title()}")

        # Switch to the new tab (Excel page)
        new_page = total_pages[1]
        new_page.bring_to_front()
        new_page.reload()
        
        new_page.wait_for_timeout(20000)
        new_page.screenshot(path="new_tab_screenshot.png")
      
        # Handle Accept button
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
                        print(f"Attempt {attempt + 1}: Accept button not found in main page or iframe")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error interacting with Accept button: {str(e)}")
                if attempt == max_retry - 1:
                    html = new_page.content()
                    print(f"HTML content after final error:\n{html}")
                    raise e
        new_page.wait_for_load_state("domcontentloaded", timeout=5000)

        new_page.reload()
        new_page.reload()
        new_page.wait_for_timeout(30000)
  
        # Click Copilot button
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
                        print(f"Attempt {attempt + 1}: Clicked Copilot button inside iframe")
                        break
                    else:
                        print(f"Attempt {attempt + 1}: Copilot button not found in main page or iframe")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error interacting with Copilot button: {str(e)}")
                if attempt == max_retry - 1:
                    html = new_page.content()
                    print(f"HTML content after final error:\n{html}")
                    raise e
                
        new_page.wait_for_timeout(5000)

        # Enter query in Copilot search bar
        for attempt in range(max_retry):
            try:
                search_bar = new_page.locator('span[role="textbox"][contenteditable="true"].fai-EditorInput__input')
                if search_bar.count() > 0:
                    search_bar.wait_for(state="visible", timeout=5000)
                    search_bar.fill("What is Project Bluefin?")
                    search_bar.press("Enter")
                    print(f"Attempt {attempt + 1}: Entered query 'What is Project Bluefin?' in search bar")
                    break
                else:
                    iframe = new_page.frame_locator("iframe")
                    search_bar = iframe.locator('span[role="textbox"][contenteditable="true"].fai-EditorInput__input')
                    if search_bar.count() > 0:
                        search_bar.wait_for(state="visible", timeout=3000)
                        search_bar.fill("What is Project Bluefin?")
                        search_bar.press("Enter")
                        print(f"Attempt {attempt + 1}: Entered query 'What is Project Bluefin?' in search bar inside iframe")
                        break
                    else:
                        print(f"Attempt {attempt + 1}: Search bar not found in main page or iframe")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Error interacting with search bar: {str(e)}")
                if attempt == max_retry - 1:
                    html = new_page.content()
                    print(f"HTML content after final error:\n{html}")
                    raise e

        print(f"New page title: {new_page.title()}")

        # Print page information
        total_pages = page.context.pages
        print(f"Total pages: {len(total_pages)}")
        for i, p in enumerate(total_pages):
            print(f"Page {i}: {p.title()}")

        new_page.pause()  # For debugging
        browser.close()