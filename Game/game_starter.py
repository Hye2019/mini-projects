'''
    Turtle Game Starter Project
    Very simple version of the game allows the user to move the turtle around screen
    and eat bugs that appear in random locations.  Your game can be very different.
    
    Please rename this file with the name of your game.
    
    Author:          (starter project by J. Fall, based on original idea from T. Dakic)
    Date:  Feb. 2019
'''
import turtle
import math
import random

from turtle_game import *


# This code is yours to use as a starting point for your project
# Hack away, make it as complex as you like, but don't make it more complicated!

def configureGame(title):
    ''' Configure a new game with a single player - return the player's turtle '''
    turtle.title(title)
    createArena()
    player = createPlayer()
    bindKeyboard(player)      # bind keyboard events to the player's turtle
    return player

def gameOver(player, bug, scoreboard, timer, score, message):
    ''' End the game, disable the player, report the game results message '''
    player.home()
    removeBug(bug)
    bindKeyboard(None)   # disable player controls
    stopTimer(timer)   # stop the timer
    displayMessage(player, message)    

def playOneGame(player, scoreboard, timer):
    '''
        Play one game with the given (pre-configured) player turtle.
        This is a VERY simple game --  player eats 3 bugs, they win, game is over.
    '''
    BUGS_TO_WIN = 3
    
    # Scoring varaibles - your game might be easier to program if these are globals, but caution: globals are evil!
    bugs_eaten = 0
    total_time = 0
    
    # Create other characters in the game
    bug = createBug()

    # The main game "loop' -- keep playing until the game is over
    while bugs_eaten < BUGS_TO_WIN:
        if isCollision(player, bug):
            bugs_eaten = bugs_eaten + 1            
            updateScoreBoard(scoreboard, bugs_eaten)
            total_time = total_time + timer.current_time
            updateTimer(timer, 0)  # restart timer from zero
            bug = replaceBug(bug)
            
        # Player's motion is driven by keyboard presses, configured by bindEvents()
        # Timer runs independently its own 'event loop' - inspect timer.current_time
        
        # Other objects in the game can be animated by updating their position here
        # For example, the bug in this game does a random walk...
        randomWalk(bug, BUG_SPEED)
    
    # When main loop exits, it means the game is over...
    message = "You WON! in %i seconds"%total_time
    gameOver(player, bug, scoreboard, timer, bugs_eaten, message)
    
    
def main():
    GAME_TITLE = "Turtle Eats Bugs -- Not Much of a Game"
    GAME_INSTRUCTIONS = "Use arrow keys to move Turtle - Eat some bugs!"
    
    player = configureGame(GAME_TITLE)
    scoreboard = createScoreBoard(GAME_INSTRUCTIONS)
    timer = createTimer()
    playOneGame(player, scoreboard, timer)
        
main()
