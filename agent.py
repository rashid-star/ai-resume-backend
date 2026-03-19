import os
import time
import requests
import pandas as pd

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import time

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LOGIN_URL = f"{BASE_URL}/login"
UPLOAD_URL = f"{BASE_URL}/upload-resume"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

FOLDER_PATH = "resumes"


# 🔐 Step 1: Login (API)
def get_token():
    res = requests.post(LOGIN_URL, json={
        "email": EMAIL,
        "password": PASSWORD
    })
    return res.json()["access_token"]


# 📤 Step 2: Upload resumes
def process_resumes(token):
    headers = {"Authorization": f"Bearer {token}"}
    results = []

    for file in os.listdir(FOLDER_PATH):
        if file.endswith(".pdf"):
            path = os.path.join(FOLDER_PATH, file)

            print(f"📄 Uploading: {file}")

            with open(path, "rb") as f:
                res = requests.post(
                    UPLOAD_URL,
                    headers=headers,
                    files={"file": f}
                )

            data = res.json()

            results.append({
                "File Name": file,
                "Best Role": data.get("best_role"),
                "Score": data.get("resume_score")
            })

    return results


# 📸 Step 3: Take dashboard screenshot
def take_screenshot():
    driver = webdriver.Chrome()

    # open login page
    driver.get("https://ai-resume-frontend-sigma.vercel.app/login")
    time.sleep(5)

    # 🔐 login (NOW works because you added name/id)
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)

    driver.find_element(By.ID, "login-btn").click()

    time.sleep(5)

    # go to dashboard
    driver.get("https://ai-resume-frontend-sigma.vercel.app/dashboard")
    time.sleep(5)

    # save screenshot
    os.makedirs("output", exist_ok=True)
    path = "output/dashboard.png"

    driver.save_screenshot(path)
    driver.quit()

    print("📸 Screenshot saved")

    return path


# 📊 Step 4: Save Excel + Image
def save_excel(results, image_path):
    df = pd.DataFrame(results)

    excel_path = "output/report.xlsx"
    df.to_excel(excel_path, index=False)

    wb = Workbook()
    ws = wb.active

    img = Image(image_path)
    ws.add_image(img, "A10")

    wb.save(excel_path)

    print("📊 Excel + Screenshot saved")


# 🚀 MAIN
if __name__ == "__main__":
    token = get_token()
    results = process_resumes(token)

    screenshot_path = take_screenshot()

    save_excel(results, screenshot_path)