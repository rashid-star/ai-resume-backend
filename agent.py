import os
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# 🔗 BASE URL (CHANGE if using Railway)
BASE_URL = os.getenv("BASE_URL")  # e.g. https://your-app-name.up.railway.app
LOGIN_URL = f"{BASE_URL}/login"
UPLOAD_URL = f"{BASE_URL}/upload-resume"

# 🔐 Your credentials
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# 📂 Folder with resumes
FOLDER_PATH = "resumes"


# 🧠 Step 1: Auto Login → Get Token
def get_token():
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }

    response = requests.post(LOGIN_URL, json=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Login successful")
        return token
    else:
        print("❌ Login failed:", response.text)
        return None


# 🧠 Step 2: Upload all resumes
def process_resumes(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    results = []

    for file in os.listdir(FOLDER_PATH):
        if file.endswith(".pdf"):
            file_path = os.path.join(FOLDER_PATH, file)

            print(f"📄 Processing: {file}")

            with open(file_path, "rb") as f:
                response = requests.post(
                    UPLOAD_URL,
                    headers=headers,
                    files={"file": f}
                )

            if response.status_code == 200:
                data = response.json()

                # 🔥 DEBUG (see actual response)
                print("API RESPONSE:", data)

                # ✅ Safe extraction
                results.append({
                    "File Name": file,
                    "Best Role": data.get("best_role"),

                    # fallback if keys missing
                    "Score": data.get("score") or "N/A",
                    "ATS Score": data.get("ats_score") or "N/A",

                    "Strengths": str(data.get("strengths") or "Not available"),
                    "Missing Skills": str(data.get("missing_skills") or "Not available"),

                    # 🔥 always capture full response
                    "Full Analysis": str(data)
                })

            else:
                print(f"❌ Error for {file}:", response.text)

    return results


# 🧠 Step 3: Save Excel
def save_to_excel(results):
    df = pd.DataFrame(results)

    os.makedirs("output", exist_ok=True)
    df.to_excel("output/results.xlsx", index=False)

    print("✅ Excel saved at output/results.xlsx")


# 🚀 MAIN AGENT FLOW
if __name__ == "__main__":
    token = get_token()

    if token:
        results = process_resumes(token)
        save_to_excel(results)
    else:
        print("❌ Agent stopped due to login failure")