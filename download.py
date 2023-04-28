import os
import requests
from zipfile import ZipFile

# Create Dataset_FIGH directory if it doesn't exist
if not os.path.exists("Dataset_FIGH"):
    os.makedirs("Dataset_FIGH")

# Define the range of patterns to download
patterns = [
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/437/949/", "start": 50678, "end": 50864},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/439/944/", "start": 48864, "end": 48992},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/956/", "start": 51555, "end": 51602},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/957/", "start": 51400, "end": 51477},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/958/", "start": 51345, "end": 51403},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/959/", "start": 51472, "end": 51501},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/960/", "start": 51492, "end": 51521},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/1143/", "start": 60043, "end": 60059},
    {"url_prefix": "https://www.federhandball.it/risultatigare/2022/440/1144/", "start": 60052, "end": 60068},
]

# Download the PDF files
for pattern in patterns:
    url_prefix = pattern["url_prefix"]
    start = pattern["start"]
    end = pattern["end"]

    for i in range(start, end + 1):
        url = f"{url_prefix}{i}.pdf"
        response = requests.get(url)

        if response.status_code == 200:
            filename = f"Dataset_FIGH/{i}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
                print(f"Downloaded and saved {filename}")
        else:
            print(f"Failed to download {i}.pdf. Status code: {response.status_code}")

# Create a zip file containing the Dataset_FIGH folder
with ZipFile("Dataset_FIGH.zip", "w") as zipf:
    for folder, _, filenames in os.walk("Dataset_FIGH"):
        for filename in filenames:
            file_path = os.path.join(folder, filename)
            zipf.write(file_path, os.path.relpath(file_path, "Dataset_FIGH"))

print("Created Dataset_FIGH.zip")
