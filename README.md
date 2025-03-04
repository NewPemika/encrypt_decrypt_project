
# Excel Encryption & Decryption Web App

## Overview

This project is a web-based application that allows users to upload Excel files and perform encryption or decryption on specific columns. The application validates the file format, ensures the correct column structure, and provides real-time feedback in case of errors.

## Features

- **Upload Excel Files**: Users can select an Excel file to encrypt or decrypt.
- **Data Validation**: Ensures the uploaded file has the correct column structure before processing.
- **Encryption & Decryption**: Sends data to an API for secure encryption or decryption.
- **Dynamic Table Display**: Shows processed data in a color-coded table (blue for encryption, green for decryption).
- **Error Handling**: Displays errors on the webpage if there are issues with the file format or API response.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend API**: Django (for processing requests)
- **Libraries**: Pandas (for handling Excel files), Fetch API (for sending requests)

---

##  Setup Instructions

### **Prerequisites**
- Python 3.13.1
- Django
- Pandas

### **Installation & Setup**

1. **Clone or Download the Repository**
   ```
   git clone https://github.com/your-repo.git
   cd your-repo
   ```

2. **Navigate to the Project Directory**
   **Important:** If you downloaded the project manually, it might have an **extra folder inside** with the same name.  

   After extraction or cloning, check your folder structure:
   ```
   dir  # Windows
   ls   # Mac/Linux
   ```
   If you see **another folder with the same name**, navigate into it **twice**:
   ```
   cd encrypt_decrypt_project-main
   cd encrypt_decrypt_project-main  # Second cd if necessary
   ```
   Verify `manage.py` exists before continuing:
   ```
   dir  # On Windows
   ls   # On macOS/Linux
   ```

3. **Run the Django server**
   ```
   python manage.py runserver
   ```
   If everything is set up correctly, you should see:
   ```
   Starting development server at http://127.0.0.1:8000/
   ```
   Open the link in your browser.

---

## Usage

1. **Upload an Excel file**
   - Click the "Choose File" button and select an Excel file.
2. **Choose an action**
   - Click "Encrypt" to encrypt data.
   - Click "Decrypt" to decrypt data.
3. **View results**
   - The processed data will be displayed in a formatted table.
   - If an error occurs, it will be shown on the page.

---



---

## API Endpoints

- **Upload File & Process Data**: `/encryption/upload/`
- **Encryption API**: `/api/encryptData`
- **Decryption API**: `/api/decryptData`

---

## 🛠 **Troubleshooting**

### ** Error: No such file or directory for `manage.py`**
#### **Issue:**
If you see this error:
```
python.exe: can't open file 'manage.py': [Errno 2] No such file or directory
```
#### **Fix:**
Ensure you are inside the correct directory:
```sh
cd encrypt_decrypt_project-main
cd encrypt_decrypt_project-main  # If needed
```
Then try running:
```sh
python manage.py runserver
```

### ** Error: Django Not Found**
If you see:
```
ModuleNotFoundError: No module named 'django'
```
It means Django is not installed. Install it using:
```sh
pip install django
```

---

## Error Handling

| Error Type        | Message                                   |
| ----------------- | ----------------------------------------- |
| Invalid File      | "Error processing file: Incorrect format" |
| Incorrect Columns | "Error: JSON format is incorrect."        |
| API Failure       | "Error: API request failed."              |

---

