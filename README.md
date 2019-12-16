# desktop-setter
Easily change your desktop background on macOS X+ or Windows 10 to a professional image matching your query. 

Requires python 3.6 or higher.

## Using desktop-setter

You can simply run 
```
python3 unsplash.py
```
to change your background using the default configurations.

You can also override default configurations by passing arguments in through the command-line.
For example, if you want an image featuring a cityscape, you can use the `query` parameter:
```
python3 unspash.py query="cityscape"
```

Additionally, you can wrap your call to unsplash.py with `watch` to automatically run this script as frequently as you desire. For example, if you wanted to change your background to a random winter-themed picture every three hours you could run the following command in your terminal:
```
watch -n 10800 "python3 unsplash.py query='winter'"
```

Note that 10800 is the number of seconds in three hours.

If you are using the zsh terminal and you do not have watch installed, you can install it using homebrew by running `brew install watch`. 

## How it works
`unsplash.py` makes a request to [UnSplash](https://api.unsplash.com/). This request returns a url for a high-resolution image which is then downloaded to the relative directory `cache/`. 
`unsplash.py` then runs a short script specific to the operating system you're using to set the desktop background to the downloaded image.


## Things left to do
 - Improve defaults for screen dimensions
 - Improve command-line argument detection and implement help/manual
 - Add capability for Linux
 - Add Siri or touchbar controls for mac
