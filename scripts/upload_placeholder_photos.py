import os
import requests

TRAITS_URL = "https://api.datadunkers.ca/api/collections/data_skaters_traits/records"
PHOTOS_URL = "https://api.datadunkers.ca/api/collections/data_skaters_photos/records"
PHOTO_PATH = "placeholder_photo.png"

def get_nicknames():
    nicknames = []
    page = 1
    while True:
        try:
            response = requests.get(TRAITS_URL, params={'page': page, 'perPage': 100})
            response.raise_for_status()
            data = response.json()
            
            items = data.get('items', [])
            if not items:
                break
                
            for item in items:
                if 'nickname' in item:
                    nicknames.append(item['nickname'])
                    
            if page >= data.get('totalPages', 1):
                break
            page += 1
        except Exception as e:
            print(f"Error fetching nicknames on page {page}: {e}")
            break
            
    return nicknames

def upload_photos(nicknames):
    if not os.path.exists(PHOTO_PATH):
        print(f"Error: Could not find {PHOTO_PATH}")
        print("Please place placeholder_photo.png in the same directory as this script, or update PHOTO_PATH.")
        return

    for nickname in nicknames:
        print(f"Uploading photo for {nickname}...")
        
        try:
            with open(PHOTO_PATH, 'rb') as f:
                # The server expects multipart/form-data for files.
                # The field names match the upload logic in index.html (nickname, real_name, photo)
                files = {
                    'photo': (os.path.basename(PHOTO_PATH), f, 'image/png')
                }
                data = {
                    'nickname': nickname,
                    'real_name': ''
                }
                response = requests.post(PHOTOS_URL, data=data, files=files)
                
                if response.status_code == 200:
                    print(f"Successfully uploaded photo for {nickname}")
                else:
                    print(f"Failed to upload photo for {nickname}. Status code: {response.status_code}")
                    print(response.text)
        except Exception as e:
            print(f"An error occurred while uploading for {nickname}: {e}")

if __name__ == "__main__":
    print("Fetching nicknames from data_skaters_traits...")
    nicknames = get_nicknames()
    
    if nicknames:
        print(f"Found {len(nicknames)} nicknames.")
        upload_photos(nicknames)
    else:
        print("No nicknames found or failed to fetch.")
