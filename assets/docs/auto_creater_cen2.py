# #pip3 install pynput
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time#,random
#xdotool getmouselocation <- get mouse position from Linux terminal 
# mouse.position is the current mouse position
keyboard = KeyboardController()
mouse = MouseController()
speed = 0.5
names = [
	'starts_with_point',
	'ends_with_point',
	'invalid_input',
	'empty_input',
	'digit'
]
numbers = [
	'10',
	'10',
	'100',
	'1',
	'50'
]
options = [
	'false',
	'false',
	'false',
	'false',
	'false'
]
substrings = [
	'[.][-][numbers][.][numbers]',
	'[-][numbers][.][numbers][.]',
	'[numbers][.,-][numbers][.,-]',
	'[something]',
	'[-][letters,signs][.][letters,signs]'
]
tams = [
	'[1][0~1][1~3][0~1][1~3]',
	'[0~1][1~3][0~1][1~3][1]',
	'[1~3][1~2][1~3][1~2]',
	'[0]',
	'[0~1][1~2][0~1][1~3]'
]

def move_and_click_and_wait(x,y,mouse,seconds=0):
	mouse.move(x,y)
	mouse.press(Button.left)
	mouse.release(Button.left)
	time.sleep(seconds)

def click_and_wait(x,y,mouse,seconds=0):
	mouse.position = (x,y) # First tab position
	mouse.press(Button.left)
	mouse.release(Button.left)
	time.sleep(seconds)

def double_click_and_wait(x,y,mouse,seconds=0):
	mouse.position = (x,y)
	mouse.click(Button.left, 2)
	time.sleep(seconds)

def command(button1,button2):
	with keyboard.pressed(button1):
		keyboard.press(button2)
		keyboard.release(button2)

def press(button):
	keyboard.press(button)
	keyboard.release(button)	

# import urllib.request
# site = 'https://globoesporte.globo.com/'
# webUrl  = urllib.request.urlopen(site)
# data = webUrl.read().decode("utf-8")
# data = str(data)

############################################################

#click_and_wait(605,751,mouse,speed) # Click to open the 4th window of the screen
# click_and_wait(277,67,mouse,speed) # Click to open the 1st window of the terminal
# click_and_wait(748,751,mouse,speed) # Click to open the 5th window of the screen
# click_and_wait(838,331,mouse,speed) # Click 'set method information' button (2nd button)
# click_and_wait(713,323,mouse,speed) # Click on the 'class name' field
# keyboard.type('Cenario2')
# press(Key.tab)
# keyboard.type('cenarios')
# press(Key.tab)
# keyboard.type('isNumber')
# press(Key.tab)
# keyboard.type('number')
# click_and_wait(797,432,mouse,speed) # Click on 'Output type'
# move_and_click_and_wait(0,115,mouse,speed) # Down to 'boolean' and click
# click_and_wait(638,488,mouse,speed) # Click on 'Next' to specify types of each parameter
# click_and_wait(812,393,mouse,speed) # Click on Parameter Output type
# move_and_click_and_wait(0,40,mouse,speed) # Down to 'String' and click
# click_and_wait(651,423,mouse,speed) # Click next to confirm method information setting
# click_and_wait(791,408,mouse,speed) # Click 'Specify test sets' button (3rd button)

# Create Test sets specified at the begin of this script
click_and_wait(72,68,mouse,speed) # Click on 'Test set name' field
click_and_wait(941,755,mouse,speed) # 7th window

for x in range(0,len(names)):
	click_and_wait(783,336,mouse,speed) # Click on 'Test set name' field
	keyboard.type( names[x] )
	press(Key.tab)
	keyboard.type( numbers[x] )
	click_and_wait(822,442,mouse,speed) # Click on Parameter 'Expected Output'
	if options[x] == 'true':
		move_and_click_and_wait(0,20,mouse,1) # Down to 'true' (1st option) and click
	else:
		move_and_click_and_wait(0,35,mouse,1) # Down to 'false' (2nd option) and click
	click_and_wait(740,500,mouse,speed) # Click 'Specify Parameters' button
	click_and_wait(712,401,mouse,speed) # Click on the 'Substrings' field
	keyboard.type( substrings[x] )
	press(Key.tab)
	keyboard.type( tams[x] )
	time.sleep(1)
	click_and_wait(667,464,mouse,speed)  # Click on the 'Confirm' button

#click_and_wait(811,507,mouse,speed) # Click 'Back' to go to home screen
#click_and_wait(826,476,mouse,speed) # Click 'Generation Tests' button