from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json
import requests
import time

# API Credentials
ACCESS_TOKEN_URL = "http://183.88.236.246:8089/api/accessToken"
ENCRYPT_URL = "http://183.88.236.246:8089/api/encryptData"
DECRYPT_URL = "http://183.88.236.246:8089/api/decryptData"
USERNAME_ENCRYPT = "API_USER_EN"
PASSWORD_ENCRYPT = "jn6aZb!Fix"
USERNAME_DECRYPT = "API_USER_DE"
PASSWORD_DECRYPT = "RY8_b6=ubU"

# Store access tokens
token_data = {
    "encrypt": {"access_token": None, "expiry_time": 0},
    "decrypt": {"access_token": None, "expiry_time": 0}
}

# Function to get an access token
def get_access_token(action):
    current_time = time.time()
    username = USERNAME_ENCRYPT if action == "encrypt" else USERNAME_DECRYPT
    password = PASSWORD_ENCRYPT if action == "encrypt" else PASSWORD_DECRYPT
    
    if token_data[action]["access_token"] is None or current_time >= token_data[action]["expiry_time"]:
        response = requests.post(ACCESS_TOKEN_URL, json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            token_data[action]["access_token"] = data.get("access_token")
            token_data[action]["expiry_time"] = current_time + 600  # Token valid for 10 minutes
        else:
            return None
    return token_data[action]["access_token"]

# Function to process encryption/decryption
def process_data(json_data, action):
    url = ENCRYPT_URL if action == "encrypt" else DECRYPT_URL
    access_token = get_access_token(action)
    
    if not access_token:
        return {"error": f"Failed to obtain {action} access token"}
    
    headers = {
        'access_token': access_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(json_data, ensure_ascii=False))
    
    return response.json() if response.status_code == 200 else {"error": f"{action.capitalize()} API failed", "message": response.text}

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        action = request.POST.get("action")

        if not file:
            return JsonResponse({"error": "No file selected"})
        if action not in ["encrypt", "decrypt"]:
            return JsonResponse({"error": "Invalid action specified"})

        try:
            df = pd.read_excel(file)
            json_data = df.to_dict(orient="records")
            processed_response = process_data(json_data, action)
            return JsonResponse({"processed_data": processed_response})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    return JsonResponse({"error": "Invalid request method"})

def index(request):
    return render(request, "index.html")
