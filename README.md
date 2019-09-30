# desktop-setter
Easily change your desktop background on macOS Mojave to a professional image matching your query. 

Uses AppleScript to 

Requires python 3.6 or higher.

## Using desktop-setter

You can simply run 
```
python change_background.py
```
to change your background using the default configurations.

You can also override default configurations by passing arguments in through the command-line.
For example, if I want an image featuring a cityscape, I can use the `query` parameter:
```
python change_background.py query="cityscape"
```

## Things left to do:
 - Improve this documentation
 - Improve defaults for screen dimensions
 - Improve command-line argument detection and implement help/manual
 
 
 ## Future Steps
 - Add capability for Windows 10 or Linux
 - Add Siri or touchbar controls for mac
