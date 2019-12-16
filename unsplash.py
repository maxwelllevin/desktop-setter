import os
import sys
import ctypes
import requests
import platform
import datetime as dt
from auth import ACCESS_KEY, SECRET_KEY
from subprocess import Popen, PIPE, call


# Global settings
cache_dir = os.path.join(os.getcwd(), "cache/")
screen_width = 3840
screen_height = 2160


# Makes a GET request to UnSplash with the provided paramters and returns a python response object
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


# Gets and saves an image matching the arguments provided. Returns the image's path on disk and the json response object
def get_and_save_image(dir=cache_dir, query='mountains, sunset', url_type='custom', format='jpg', access_key=ACCESS_KEY, fit='clip', width=screen_width, height=screen_height, featured='true', orientation='landscape', filename=None):
    response = get_random_image(query=query, format=format, access_key=access_key, featured=featured, orientation=orientation, fit=fit, width=width, height=height)
    if (response.status_code != 200):
        print(f"Error: Response failed with status code {response.status_code}")
        quit(response.status_code)
    filename = extractFilename(response.json(), dir, format) if (filename == None) else filename
    save_file(response.json()['urls'][url_type], filename=filename)
    return filename, response.json()


# Builds a filename from a json response object. The filename is the id of the image as provided by the UnSplash api response.
def extractFilename(response_json, dir, format):
    return dir + response_json['id'] + '.' + format


# Saves the image at the given url to disk with the provided filename
def save_file(url, filename):
    os.makedirs(cache_dir, exist_ok=True)
    r = requests.get(url, allow_redirects=True)
    open(f'{filename}', 'wb').write(r.content)


# time_kwargs are arguments to use in the datetime.timedelta() function. 
# Ex: time_kwargs={'minutes': 30} would set the 'ago' variable to 30 minutes in the past
def clear_old_cache(time_kwargs={'hours': 1}):
    now = dt.datetime.now()
    ago = now - dt.timedelta(**time_kwargs)
    for root, dirs, files in os.walk(cache_dir):  
        for fname in files:
            path = os.path.join(root, fname)
            st = os.stat(path)    
            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if mtime < ago:
                print(f"Removing old file: {path}")
                Popen(f"rm {path}", shell=True)



def set_background(filename):
    """
    Sets the desktop background.
    """
    if platform.system() == "Darwin":
        # Applescript:
        cmd = f'/usr/bin/osascript<<END\ntell application "Finder"\nset desktop picture to POSIX file "{filename}"\nend tell\nEND'
        Popen(cmd, shell=True)
        call(["killall Dock"], shell=True)
        return
    if platform.system() == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filename, 0)
        return


# Defines the default keyword arguments used in the GET request to unsplash.com
def default_param_kwargs():
    return {
        'featured':'true', 
        'query':'mountains, sunset',
        'orientation':'landscape',
        'format':'jpg',
        'fit':'clip',
        'width':screen_width,
        'height':screen_height
    }


# Unpacks command-line arguments.
# Arguments should be made in the form of: key="value"
# Ex the following line would change the desktop background to an image matching the query of snowy mountains:
#   python change_background.py query="snowy mountains"
def read_args(argv):
    kwargs = default_param_kwargs()
    if len(argv) <= 1:  # No parameters passed in, use the defaults
        return kwargs
    for arg in argv[1:]:
        arg = arg.split('=')
        if len(arg) == 1:
            print(f"WARNING! Skipping illegal argument '{arg[0]}'. If you would like to use this parameter, please use the format: myParameter='my param value'")
            continue
        param, value = arg[0], arg[1].replace("'", '').replace('"', '')
        kwargs[param] = value
    return kwargs


if __name__ == "__main__":
    clear_old_cache({'hours': 24})
    kwargs = read_args(sys.argv)
    filename, image_json = get_and_save_image(**kwargs)
    success = set_background(filename)
    print(f"Set file: {filename} as desktop image at {str(dt.datetime.now())}")
    print(f"Image Description: {image_json['description']}")

