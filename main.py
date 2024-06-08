import os
import yaml

from datetime import datetime, timedelta
from playwright.sync_api import Playwright, sync_playwright

if not os.path.exists('secrets.yaml'):
    raise Exception('secrets.yaml is missing')


def read_secrets(file_path):
    with open(file_path, 'r') as file:
        secrets = yaml.safe_load(file)
    return secrets


secrets = read_secrets('secrets.yaml')


def run(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()

    # Get today's date
    today = datetime.today()

    # Calculate the start of the previous week
    start_of_prev_week = today - timedelta(days=today.weekday() + 7)

    # Calculate the end of the previous week
    end_of_prev_week = start_of_prev_week + timedelta(days=6)

    # Format dates in 'yyyy-mm-dd' format
    start_of_prev_week_str = start_of_prev_week.strftime('%Y-%m-%d')
    end_of_prev_week_str = end_of_prev_week.strftime('%Y-%m-%d')

    # Construct output file path and filename
    directory = os.path.join(os.path.expanduser('~'),
                             secrets['directory'] % today.strftime('%Y').strip())
    filename = f"{today.strftime('%Y-%m-%d')} Timesheet {start_of_prev_week_str} - {end_of_prev_week_str}.pdf"
    full_path = os.path.join(directory, filename)

    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    page = context.new_page()
    page.goto("https://accounts.toggl.com/track/login/")
    page.get_by_label("Email").click()
    page.get_by_label("Email").fill(secrets['email'])
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(secrets['password'])
    page.get_by_role("button", name="Log in via email").click()
    page.wait_for_url("https://track.toggl.com/**")
    page.goto("https://track.toggl.com/reports/summary/2274727/period/prevWeek")
    page.get_by_role("button", name="Export").click()

    with page.expect_download() as download_info:
        page.get_by_text("Download PDF").click()

    download = download_info.value

    # Save the download with the specified file path and name
    download.save_as(full_path)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
