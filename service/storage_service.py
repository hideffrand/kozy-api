import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, request, jsonify
import os

# Initialize Firebase app
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-app-id.appspot.com'
})

bucket = storage.bucket()

config = {
    "apiKey": "AIzaSyDCQ_aku16nTxmAbfewnEAAaDxL2OQcfv0",
    "authDomain": "arexpo-f3d8d.firebaseapp.com",
    "projectId": "arexpo-f3d8d",
    "storageBucket": "arexpo-f3d8d.appspot.com",
    "messagingSenderId": "888596058713",
    "appId": "1:888596058713:web:20a326e43ccecb290e9748",
    "measurementId": "G-K7C3N1L8WN"
}


def get_all_files(folder_name):
    try:
        blobs = bucket.list_blobs(prefix=folder_name)
        files_data = []
        for blob in blobs:
            files_data.append({
                "fileName": blob.name,
                "url": blob.public_url
            })
        return files_data
    except Exception as e:
        print("Error fetching files:", e)
        return []


def upload_file(file_to_upload, file_type):
    try:
        if file_type == "image":
            allowed_types = ["image/png", "image/jpeg",
                             "image/jpg", "image/webp"]
            if file_to_upload.content_type not in allowed_types:
                return "Invalid file type. Please upload a PNG, JPEG, JPG, or WEBP image."

            blob = bucket.blob(f"gallery/{file_to_upload.filename}")
            blob.upload_from_file(file_to_upload)
            return "Image uploaded successfully!"
        else:
            allowed_types = ["application/pdf", "application/msword"]
            if file_to_upload.content_type not in allowed_types:
                return "Invalid file type. Please upload a PDF or DOC file."

            blob = bucket.blob(f"documents/{file_to_upload.filename}")
            blob.upload_from_file(file_to_upload)
            return "Document uploaded successfully!"
    except Exception as e:
        print("Error while uploading file:", e)
        return "Failed to upload file"


def delete_file(file_name, file_type):
    try:
        folder = "gallery" if file_type == "image" else "documents"
        blob = bucket.blob(f"{folder}/{file_name}")
        blob.delete()
        return "File deleted successfully!"
    except Exception as e:
        print("Error deleting file:", e)
        return "Error deleting file"
