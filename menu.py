from time import sleep
from math import ceil
import curses, os #curses is the interface for capturing key presses on the menu, os launches the files
screen = curses.initscr() #initializes a new window for capturing key presses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() # Lets you use colors when highlighting selected menu option
screen.keypad(1) # Capture input from keypad

# Change this to use different colors when highlighting
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair( 1 )
n = curses.A_NORMAL

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"

# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):

  # work out what text to display as the last menu option
  if parent is None:
    lastoption = "Exit"
  else:
    lastoption = "Return to %s menu" % parent['title']

  optioncount = len(menu['options']) # how many options in this menu

  max_row = 10 if optioncount > 10 else optioncount #max number of rows
  screen.border(0)
  box = curses.newwin( max_row + 3, 100, 1, 1 )
  box.box()

  pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
  oldpos=None # used to prevent the screen being redrawn every time
  x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

  pages = int( ceil( optioncount / max_row ) )
  page = 1
  
  # Loop until return key is pressed
  while x !=ord('\n'):

    if pos != oldpos:
      oldpos = pos
      screen.addstr(2,2, menu['title'], curses.A_STANDOUT) # Title for this menu
      screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu    

    x = screen.getch() # Gets user input

    # What is user input?
    if x >= ord('1') and x <= ord(str('9')):
      pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
    elif x == 258: # down arrow
      if page == 1:
            if pos < max_row:
                pos = pos + 1
            else:
                if pages > 1:
                    page = page + 1
                    pos = 1 + ( max_row * ( page - 1 ) )
      elif page == pages:
          if pos < optioncount:
               pos = pos + 1
      else:
          if pos < max_row + ( max_row * ( page - 1 ) ):
              pos = pos + 1
          else:
              page = page + 1
              pos = 1 + ( max_row * ( page - 1 ) )
    elif x == 259: # up arrow
      if page == 1:
            if pos > 0:
                pos = pos - 1
      else:
          if pos > ( 1 + ( max_row * ( page - 1 ) ) ):
              pos = pos - 1
          else:
              page = page - 1
              pos = max_row + ( max_row * ( page - 1 ) )
    elif x == 260: # left arrow
      if page > 1:
            page = page - 1
            pos = 1 + ( max_row * ( page - 1 ) )
    elif x == 261: # right arrow
      if page < pages:
            page = page + 1
            pos = ( 1 + ( max_row * ( page - 1 ) ) )

    box.erase()
    screen.border( 0 )
    box.border( 0 )

    for i in range( 0 + (max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ))):
        if optioncount == 0:
            box.addstr( 1, 1, "There aren't strings",  h )
        else:
            if ( i + ( max_row * ( page - 1 ) ) == pos + ( max_row * ( page - 1 ))):
              if (i == optioncount):
                box.addstr( i + 1 - ( max_row * ( page - 1 ) ), 2, lastoption, h )
              else:
                box.addstr( i + 1 - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + menu['options'][i]['title'], h )         
            else:
              if (i == optioncount):
                box.addstr( i + 1 - ( max_row * ( page - 1 ) ), 2, lastoption, n )
              else:
                box.addstr( i + 1 - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + menu['options'][i]['title'], n )   
            if (i == optioncount ):
                break

    screen.refresh()
    box.refresh()

  # return index of the selected item
  screen.erase()
  screen.border(0)
  return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
  optioncount = len(menu['options'])
  exitmenu = False
  while not exitmenu: #Loop until the user exits the menu
    getin = runmenu(menu, parent)
    if getin == optioncount:
        exitmenu = True
    elif menu['options'][getin]['type'] == COMMAND:
      curses.def_prog_mode()    # save curent curses environment
      screen.clear() #clears previous screen
      os.system(menu['options'][getin]['command']) # run the command
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)
    elif menu['options'][getin]['type'] == MENU:
          screen.clear() #clears previous screen on key press and updates display based on pos
          processmenu(menu['options'][getin], menu) # display the submenu
          screen.clear() #clears previous screen on key press and updates display based on pos
    elif menu['options'][getin]['type'] == EXITMENU:
          exitmenu = True

# Main program
# processmenu(menu_data)
curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('cls')