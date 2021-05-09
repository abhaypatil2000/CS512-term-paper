# Requirements  
`freegames` module is necessary to run this program  
Run `pip install freegames` to install the same

# Execution  
In main function of this code, adjust the values of mid_time, end_time  
from step [0, mid_time) scatter mode and from step [mid_time, end_time) attack mode  
If scatter mode to be disabled completely then set `want_timeout` to `False`, in main function  
In scatter mode, ghosts will be colored green and won't kill pacman even on contact.  
In chase mode, ghosts will be colored in shades of brown color.  

Run `python3 code.py` to run the game  

The user will be prompted to enter the type of game to be played (options will be displayed in the terminal), enter the option number and press enter.  

# Code structure  
File `code.py` contains the main logic  
File `map.py` contains the map in the question, it can be modified independently. But the dimensions must be same.

In the 3rd part i.e., A* with 2 cordinating players, the darkest color will be the leader and the 2nd darkest color will be the follower and rest 2 will work independently.

In the 4th part i.e., A* will 4 cordinating players, the darkest will play first, then second darkest will make adjustments accordingly, and the third darkest will make adjustments according to first 2 and lightest color will make adjustments according to all the other 3 ghosts.

There are certain parameters used by the ghosts which can be tweaked in the code. They are as follows:  
1. **first parameter:** This parameter does this.  
2. **second parameter:** This parameter does this.  

# Instructions to play the game:  
Use the arrow keys to redirect the pacman.  
The arrow keys need to be pressed when the position of pacman is stationary, previous button pressed are discarded. Hence to play the game the best option is to spam the direction keys when aa turn is about to come.  

Else there is a chance that the keystrokes are ignored.