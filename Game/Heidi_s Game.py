'''
    Turtle Game
    
    Author: Heidi Ye (starter project by J. Fall, based on original idea from T. Dakic)
    Date:  Feb. 2019
'''
import turtle
import math
import random

from turtle_game import *

def configureGame(title):
    ''' Configure a new game with a single player - return the player's turtle '''
    turtle.title(title)
    createArena()
    head = createPlayer()
    bindKeyboard(head)      # bind keyboard events to the player's turtle
    return head

def gameOver(head, bug, scoreboard, timer, message):
    ''' End the game, disable the player, report the game results message '''
    head.home()
    removeBug(bug)
    bindKeyboard(None)   # disable player controls
    stopTimer(timer)   # stop the timer
    displayMessage(head, message)
    
def followHead(snake):
    lastSnake = len(snake)
    for i in range (len(snake) - 1):
        lastSnake = lastSnake - 1 
        snake[(lastSnake)].goto(snake[(lastSnake - 1)].position()-(20,20))

def playOneGame(head, scoreboard, timer):
    #Global Variables
    TURTLES_TO_WIN = 3
    turtles_captured = 0
    total_time = 0
    ENEMY_SPEED = 5
    
    # Game Characters 
    yellowTurtle = createBug()
    movingEnemy = createEnemy()
    staticEnemy = createStaticEnemy()
    
    # List that holds recruited turtles 
    snake = [head]
    
    while turtles_captured < TURTLES_TO_WIN:
        randomWalk(yellowTurtle, BUG_SPEED) #starts game with moving target
        randomWalk(movingEnemy, ENEMY_SPEED) #starts game with moving enemy
        followHead(snake) #allows captured turtle to follow the player  
        if isOutOfBounds(head) or isCollision(head,movingEnemy) or isCollision(head,staticEnemy):
            loseMessage = "You CRASHED - Game Over! "
            updateScoreBoard(scoreboard, turtles_captured)
            gameOver(head, yellowTurtle, scoreboard, timer, loseMessage)      
        elif isCollision(head, yellowTurtle):
            randomWalk(movingEnemy, ENEMY_SPEED)
            turtles_captured = turtles_captured + 1
            updateScoreBoard(scoreboard, turtles_captured)
            total_time = total_time + timer.current_time
            yellowTurtle = replaceBug(yellowTurtle)
            snake.append(createBug())
            createStaticEnemy()
            
    winMessage = "You WON in %i seconds!"%total_time
    gameOver(head, yellowTurtle, scoreboard, timer, winMessage)
        
def main():
    GAME_TITLE = "Turtle Recruit"
    GAME_INSTRUCTIONS = '''Use arrows to move the blue turtle.
Capture 3 yellow turtles to win!
But don't crash into walls or sqaure enemies!'''
    
    head = configureGame(GAME_TITLE)
    scoreboard = createScoreBoard(GAME_INSTRUCTIONS)
    timer = createTimer()
    playOneGame(head, scoreboard, timer)

main()

