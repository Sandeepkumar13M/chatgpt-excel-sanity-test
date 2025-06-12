import pytest
from patchright.sync_api import sync_playwright, Page, Browser 

def test_sensitive_text():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://m365.cloud.microsoft/")
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_selector('//*[@id="i0116"]').fill("devtest@acuvity.dev")
        page.wait_for_selector('//*[@id="idSIButton9"]').click()
        page.wait_for_selector('//*[@id="passwordEntry"]').fill("TLpmocomKJ6GUY8qMCzV")
        page.wait_for_selector('//*[@id="view"]/div/div[5]/button').click()
        page.wait_for_selector('//*[@id="view"]/div/div[5]/button[2]').click()

        # Wait for the Excel button and capture the new tab
        with page.expect_popup() as popup_info:
            page.wait_for_selector('//*[@id="create-new-list"]/div[2]/div[3]/div/div[1]').click()
        new_page = popup_info.value

        # Wait for the new tab to fully load
        new_page.wait_for_load_state("networkidle")
        new_page.wait_for_load_state("load")
        new_page.wait_for_load_state("domcontentloaded")

        
        # Click the "Accept" button in the new tab using XPath
        # new_page.wait_for_selector("//button[text()='Accept']").click()

        # Pause to inspect the new tab (remove in production)


        new_page.locator('#Copilot').click()




        new_page.pause()


#------------------------------------------------------------------------------------------------------


# def test_sensitive_text():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto("https://excel.cloud.microsoft/")
#         page.wait_for_selector('//*[@id="enterpriseShellHeader"]/div/button').click()
#         page.wait_for_selector('//*[@id="i0116"]').fill("devtest@acuvity.dev")
#         page.wait_for_selector('//*[@id="idSIButton9"]').click()
#         page.wait_for_selector('//*[@id="passwordEntry"]').fill("TLpmocomKJ6GUY8qMCzV")
#         page.wait_for_selector('//*[@id="view"]/div/div[5]/button').click()
#         page.wait_for_selector('//*[@id="view"]/div/div[5]/button[2]').click()
#         page.wait_for_selector('//*[@id="root"]/div/div/div[3]/div[1]/div/div/div/div/div[2]/button').click()
#         page.pause()
#         page.wait_for_selector("//button[text()='Home']").click()

#         # page.wait_for_selector('//*[@id="Copilot"]').click()
       

#         page.pause() 




#-------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------


# def test_sensitive_text():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         # ─── 1) LOGIN TO M365 ────────────────────────────────────────────────
#         page.goto("https://m365.cloud.microsoft/")
#         page.get_by_role("button", name="Sign in").click()
#         page.locator('//*[@id="i0116"]').fill("devtest@acuvity.dev")
#         page.locator('//*[@id="idSIButton9"]').click()
#         page.locator('//*[@id="passwordEntry"]').fill("TLpmocomKJ6GUY8qMCzV")
#         page.locator('//*[@id="view"]/div/div[5]/button').click()
#         page.locator('//*[@id="view"]/div/div[5]/button[2]').click()

#         # ─── 2) OPEN EXCEL ONLINE ───────────────────────────────────────────
#         with page.expect_popup() as popup_info:
#             page.locator('//*[@id="create-new-list"]/div[2]/div[3]/div/div[1]').click()
#         excel_page = popup_info.value
#         excel_page.wait_for_load_state("domcontentloaded", timeout=1000)

#         # ─── 3) TRIGGER YOUR APP’S “ACTIVE-STATE” DIALOG ────────────────────
#         # (this is whatever action causes that separate window to pop up)
#         with context.expect_event("page") as dialog_info:
#             excel_page.click("//button[text()='Accept']")  # ← your trigger here
#         dialog_page = dialog_info.value

#         # ─── 4) CLICK “ACCEPT” ON THE DIALOG ────────────────────────────────
#         dialog_page.wait_for_load_state("domcontentloaded", timeout=1000)
#         dialog_page.click("button:has-text('Accept')")
#         # if it doesn’t auto-close:
#         dialog_page.close()

#         # ─── 5) RETURN TO EXCEL AND CONTINUE ───────────────────────────────
#         excel_page.bring_to_front()
#         # wait for the real workbook URL pattern
#         excel_page.wait_for_url("**/doc2.aspx?**", timeout=30_000)

#         # …now you can interact with the online workbook…
#         assert "Excel" in excel_page.title()



