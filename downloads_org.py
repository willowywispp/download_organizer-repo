#!/usr/bin/env python3
import os
import shutil
import time

folder = os.path.expanduser("~/Downloads")

date = time.strftime("%d/%m %H:%M")

categories = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images", ".webp": "Images",
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos",
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".py": "Programs", ".html": "Programs", "js": "Programs", ".css": "Programs"
}

try:
    for filename in os.listdir(folder):


        if os.path.isfile(os.path.join(folder, filename)):
            extension = os.path.splitext(filename)[1]
            category = categories.get(extension, "Other")

            destination = os.path.join(folder, category)
            os.makedirs(destination, exist_ok=True)

            shutil.move(os.path.join(folder, filename), destination)

            if category == "Other":
                print(f"File type {extension} moved to 'Other'")

except Exception as e:
    with open("/home/willow/work/download_organizer/error.txt", "a", encoding="utf-8") as f:
        f.write(f"\nError at {date}: {e}")


