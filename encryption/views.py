from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json
import requests
import time

# API Endpoints
ACCESS_TOKEN_URL = "http://183.88.236.246:8089/api/accessToken"
ENCRYPT_URL = "http://183.88.236.246:8089/api/encryptData"
DECRYPT_URL = "http://183.88.236.246:8089/api/decryptData"

# API Credentials
USERNAME_ENCRYPT = "Encryption"
ROLE_ENCRYPT = "Encrypt"
USERNAME_DECRYPT = "Decryption"
ROLE_DECRYPT = "Decrypt"

# Store access tokens with expiry
token_data = {
    "encrypt": {"token": None, "expiry_time": 0},
    "decrypt": {"token": None, "expiry_time": 0}
}

# Function to get an access token
def get_access_token(action):
    current_time = time.time()
    username = USERNAME_ENCRYPT if action == "encrypt" else USERNAME_DECRYPT
    role = ROLE_ENCRYPT if action == "encrypt" else ROLE_DECRYPT
    
    if token_data[action]["token"] is None or current_time >= token_data[action]["expiry_time"]:
        response = requests.post(ACCESS_TOKEN_URL, json={"username": username, "role": role})
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")
            token_data[action]["token"] = token
            token_data[action]["expiry_time"] = current_time + 600
        else:
            print("Failed to obtain access token:", response.text)
            return None
    return token_data[action]["token"]

# Function to process encryption/decryption
def process_data(json_data, action):
    url = ENCRYPT_URL if action == "encrypt" else DECRYPT_URL
    access_token = get_access_token(action)
    
    if not access_token:
        print(f"Failed to obtain {action} access token")
        return {"error": f"Failed to obtain {action} access token"}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    print("Request Headers:", headers)
    print("Request Payload:", json.dumps(json_data, ensure_ascii=False))
    response = requests.post(url, headers=headers, data=json.dumps(json_data, ensure_ascii=False))
    if response.status_code == 200:
        print(f"{action.capitalize()} Success:", response.json())
        return response.json()
    else:
        print(f"{action.capitalize()} Failed:", response.status_code, response.text)
        return {"error": f"{action.capitalize()} API failed", "message": response.text}

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
            print("Error:", str(e))
            return JsonResponse({"error": str(e)})
    
    return JsonResponse({"error": "Invalid request method"})

def index(request):
    return render(request, "index.html")
