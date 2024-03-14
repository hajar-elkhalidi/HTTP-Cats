import requests as r

def download_picture(status):
    if not status.isdigit() or int(status) < 100 or int(status) >= 600:
        return "Invalid status code! Please provide a valid HTTP status code."

    url = f"https://http.cat/{status}.jpg"
    filename = f"{status}.jpg"
    response = r.get(url)
    
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Picture downloaded successfully as '{filename}'.")
        return filename
    else:
        print(f"Failed to download picture from '{url}'. Status code: {response.status_code}")
        return "Try another status code!"