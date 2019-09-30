from auth import ACCESS_KEY, SECRET_KEY
from subprocess import Popen, PIPE, call
import requests
import os


cache_dir = os.path.join(os.getcwd(), "cache/")
screen_width = 2560
screen_height = 1600

os.makedirs(cache_dir, exist_ok=True)


def get_random_image(featured='true', query='mountains, sunset', orientation='landscape', format='jpg', fit='clip', width=screen_width, height=screen_height, access_key=ACCESS_KEY):
    params={'client_id': access_key,
            'featured': featured,
            'query': query,
            'fm': format,
            'orientation': orientation,
            'fit': fit,
            'w': width,
            'h': height} 
    headers={'Accept-Version': 'v1'}
    return requests.get('https://api.unsplash.com/photos/random', params=params, headers=headers)


def extractFilename(response_json, dir, format):
    return dir + response_json['id'] + '.' + format


def save_file(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(f'{filename}', 'wb').write(r.content)


def save_random_image(dir=cache_dir, query='mountains, sunset', url_type='full', format='jpg', access_key=ACCESS_KEY, fit='clip', width=screen_width, height=screen_height, featured='true', orientation='landscape', filename=None):
    response = get_random_image(query=query, format=format, access_key=access_key, featured=featured, orientation=orientation, fit=fit, width=width, height=height)
    if (response.status_code != 200):
        print(f"Error: Response failed with status code {response.status_code}")
        return
    filename = extractFilename(response.json(), dir, format) if (filename == None) else filename
    save_file(response.json()['urls'][url_type], filename=filename)
    return filename, response.json()


def set_background(filename):
    # Formatting for the AppleScript command needs to be precise
    cmd = f'/usr/bin/osascript<<END\ntell application "Finder"\nset desktop picture to POSIX file "{filename}"\nend tell\nEND'
    try:
        Popen(cmd, shell=True)
        call(["killall Dock"], shell=True)
    except:
        return False
    return True


if __name__ == "__main__":
    filename, image_json = save_random_image(query="mountains, ice")
    # print(image_json['description'])
    print(image_json['user']['username'])
    # print(image_json['exif'])
    print(f"Saved file: {filename}")
    print("Success" if set_background(filename) else "Failure")
