# desktop-setter
Easily change your desktop background on macOS Mojave to a professional image matching your query. 

Requires python 3.6 or higher.

## Using desktop-setter

You can simply run 
```
python3 change_background.py
```
to change your background using the default configurations.

You can also override default configurations by passing arguments in through the command-line.
For example, if I want an image featuring a cityscape, I can use the `query` parameter:
```
python3 change_background.py query="cityscape"
```

Additionally, you can wrap your call to change_background.py with `watch` to automatically run this script as frequently as you desire. For example, if you wanted to change your background to a random winter-themed picture every three hours you could run the following command in your terminal:
```
watch -n 10800 "python3 change_background.py query='winter'"
```

Note that 10800 is the number of seconds in three hours.

If you are using the zsh terminal and you do not have watch installed, you can install it using homebrew by running `brew install watch`. 

## How it works
`change_background.py` makes a request to [UnSplash](https://api.unsplash.com/). This request returns a url for a high-resolution image which is then downloaded to the relative directory `cache/`. 
`change_background.py` then runs a short AppleScript program to then set the desktop background to the downloaded image.


## Things left to do
 - Improve this documentation
 - Improve defaults for screen dimensions
 - Improve command-line argument detection and implement help/manual
 
 
 ## Future Steps
 - Add capability for Windows 10 or Linux
 - Add Siri or touchbar controls for mac
