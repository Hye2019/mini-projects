'''
    Turtle Game Nano-framework
    
    A set basic functionality for games where the 'Player' controls a turtle,
    moving it around within a bounded 'Arena' and interacting with 'Bugs'
    
    Turtle is controlled by three keys: FOWARD, LEFT, RIGHT
    
    Author: J. Fall (based on original idea from T. Dakic)
    Date:  Feb. 2019
'''
import turtle
import math
import random

# GLOBAL DATA DEFINITIONS
TURTLE_BODY_SIZE = 20  # standard size of built-in turtle shapes, in pixels.

# Arena dimensions, colour, border
ARENA_LENGTH  = 300
ARENA_BREADTH = 300
ARENA_MAX_X = ARENA_LENGTH//2
ARENA_MIN_X = -ARENA_MAX_X
ARENA_MAX_Y = ARENA_BREADTH//2
ARENA_MIN_Y = -ARENA_MAX_Y
ARENA_COLOUR = 'light green'
ARENA_BORDER_COLOUR = 'black'
ARENA_BORDER_WIDTH = 3

# Scoreboard / Timer font size and colour
FONT_SIZE = 14   
FONT_COLOR = 'red'
# Definitions for the game 'Score Board'
SCOREBOARD_X = ARENA_MIN_X
SCOREBOARD_Y = ARENA_MAX_Y + 3*FONT_SIZE
SCOREBOARD_TEXT = 'Score: '
# Definition for a game 'Timer'
TIMER_X = ARENA_MIN_X
TIMER_Y = ARENA_MIN_Y - FONT_SIZE*1.5
TIMER_TEXT = 'Time: '
TIMER_START = 0
TIMER_RATE  = 1    #  seconds between timer ticks (can be factional, must be positive)


# Player's turtle defintions
STEP_SIZE = 10   # how many units does the player move in one step forward (speed)
TURN_ANGLE = 30  # how many degrees does one keypress spin the player
PLAYER_SCALE = 1 # scaling factor for size of player's turtle
PLAYER_SHAPE = 'turtle'
PLAYER_COLOUR = 'blue'
# Key bindings for player's controls
FORWARD = 'Up'
LEFT = 'Left'
RIGHT = 'Right'

# Size, shape, colour of 'bugs' in the game
BUG_SCALE = 0.3
BUG_SHAPE = 'circle'
BUG_COLOUR = 'black'
BUG_SPEED = 2


##### HELPER FUNCTIONS #####

def drawRectangle(t, length, breadth):
    ''' draw a left-handed rectangle, lengthxbreadth '''
    for L in range(2):
        t.forward(length)
        t.left(90)
        t.forward(breadth)
        t.left(90)

def turtleRadius(t):
    ''' return the radius of an imaginary cicle enclosing turtle t's shell '''
    width, height, outline = t.shapesize()
    return (width + height) / 2 * TURTLE_BODY_SIZE


##### ARENA #####
        
def drawArenaBoundary():
    ''' draw game arena's boundary line '''
    t = turtle.Turtle()
    t.penup()
    t.speed(0)
    t.hideturtle()
    t.pencolor(ARENA_BORDER_COLOUR)
    t.pensize(ARENA_BORDER_WIDTH)
    t.setposition(ARENA_MIN_X, ARENA_MIN_Y)
    t.pendown()
    drawRectangle(t, ARENA_LENGTH, ARENA_BREADTH)
    
def createArena():
    ''' create the game's areana and return its screen '''
    screen = turtle.Screen()
    screen.screensize(ARENA_BREADTH*1.5, ARENA_LENGTH*1.5)
    screen.bgcolor(ARENA_COLOUR)
    drawArenaBoundary()
    return screen

def randomArenaCoordinate():
    ''' return random coordinate (x,y) well within the game's playing Arena '''
    x = random.randint(int(ARENA_MIN_X*0.9), int(ARENA_MAX_X*0.9))
    y = random.randint(int(ARENA_MIN_Y*0.9), int(ARENA_MAX_Y*0.9))
    return x, y


##### SCOREBOARD / MESSAGING #####

def displayMessage(t, message, *args):
    ''' Display the given message and optional arguments with the given turtle '''
    for arg in args:
        message = "%s %s"%(message, arg)
        
    t.write(message, False, align="left", font=("Arial",FONT_SIZE, "normal"))

def updateScoreBoard(scoreboard, score, text=SCOREBOARD_TEXT):
    ''' Replace previous score with the given score on the scoreboard '''
    scoreboard.undo()  # remove previous scorebord text
    displayMessage(scoreboard, text, score)
    
def createScoreBoard(instructions=None, text=SCOREBOARD_TEXT):
    ''' return a turtle that acts as the 'scoreboard'; displayed with optional instructions '''
    scoreboard = turtle.Turtle()
    scoreboard.color(FONT_COLOR)
    scoreboard.pensize(3)
    scoreboard.hideturtle()
    scoreboard.penup()
    scoreboard.setposition(SCOREBOARD_X, SCOREBOARD_Y)
    if instructions:
        displayMessage(scoreboard, instructions)
        scoreboard.setposition(scoreboard.xcor(), scoreboard.ycor()-FONT_SIZE*1.5)
    displayMessage(scoreboard, text, 0)
    return scoreboard


##### TIMER #####
def updateTimer(timer, time, text=None):
    ''' Replace previous text / time on the timer with the given text and time '''
    timer.undo()  # remove previous scorebord text
    timer.current_time = time
    if text:
        timer.text = text
    displayMessage(timer, timer.text, timer.current_time)

def stopTimer(timer):
    ''' Stop or pause the timer '''
    timer.is_running = False

def startTimer(timer):
    ''' Start or restart a stopped timer '''
    # Callback to update the timer every time it 'ticks' (every TIMER_RATE seconds)
    def tick():
        if timer.is_running:
            updateTimer(timer, timer.current_time+timer.step)
            turtle.ontimer(tick, TIMER_RATE*1000)  # set callback for next 'tick'
    # Start the timer simply by forcing it's first 'tick'
    timer.is_running = True
    tick()
    
def createTimer(text=TIMER_TEXT, start_time=TIMER_START, step=1):
    ''' return a turtle that acts as a 'timer'; displayed with optional text '''
    timer = turtle.Turtle()
    timer.color(FONT_COLOR)
    timer.pensize(3)
    timer.hideturtle()
    timer.penup()
    timer.setposition(TIMER_X, TIMER_Y)

    # Additional 'state' information stored with the timer
    timer.text = text
    timer.step = step
    timer.current_time = start_time-step  # the actual time-keeping variable.
    displayMessage(timer, timer.text, timer.current_time)

    # Start the timer ticking
    startTimer(timer)
    
    return timer


##### BUG-related OPERATIONS #####
        
def createBug():
    ''' return a 'bug' positioned at a random location on the screen '''
    bug = turtle.Turtle()
    bug.penup()
    bug.color('yellow')
    bug.shape('turtle')
    bug.shapesize(1,1)
    bug.setposition(randomArenaCoordinate())
    return bug

def createEnemy():
    ''' return a 'bug' positioned at a random location on the screen '''
    bug = turtle.Turtle()
    bug.penup()
    bug.color('red')
    bug.shape('square')
    bug.shapesize(1,1)
    bug.setposition(randomArenaCoordinate())
    return bug

def createStaticEnemy():
    ''' return a 'bug' positioned at a random location on the screen '''
    bug = turtle.Turtle()
    bug.penup()
    bug.color('dark red')
    bug.shape('square')
    bug.shapesize(1.5,1.5)
    bug.setposition(randomArenaCoordinate())
    return bug

def removeEnemy(enemy):
    ''' remove the given bug from the game '''
    enemy.hideturtle()
    del enemy
    
def replaceEnemy(enemy):
    ''' remove the oldBug from the game and return a freshly created, random bug '''
    removeEnemy(enemy)
    newEnemy = createEnemy()
    return newEnemy

def removeBug(bug):
    ''' remove the given bug from the game '''
    bug.hideturtle()
    del bug

def replaceBug(oldBug):
    ''' remove the oldBug from the game and return a freshly created, random bug '''
    removeBug(oldBug)
    newBug = createBug()
    return newBug


##### TURTLE ANIMATION #####

def randomWalk(t, step_size=1):
    ''' Random walk turtle t up to 1 'step-size' step in any direction '''
    x,y = t.position()
    x_min, x_max = int(x-step_size), int(x+step_size)
    new_x = random.randint( x_min, x_max )
    y_min, y_max = int(y-step_size), int(y+step_size)
    new_y = random.randint(y_min, y_max)
    t.setposition(new_x, new_y)
    bounceOffBoundary(t)  # keep the bug in bounds

def isCollision(t1, t2):
    ''' return True iff turtles t1 and t2 have collided, False otherwise '''
    # distance between turtle centres:  Pythagoreas (a**2 + b**2 == c**2)
    dist = math.sqrt((t1.xcor()-t2.xcor())**2 + (t1.ycor()-t2.ycor())**2)
    # combined length from turtle centres to edge of shells
    combined_size = turtleRadius(t1) + turtleRadius(t2)
    return dist < combined_size  # True if shells overlap, False otherwise!

# Check / Enforce Arena boundaries
def isOutTop(t):
    ''' return True if t is outside top of Arena, False otherwise '''
    top_edge = ARENA_MAX_Y - turtleRadius(t)
    return t.ycor() > top_edge

def isOutBottom(t):
    ''' return True if t is outside bottom of Arena, False otherwise '''
    bottom_edge = ARENA_MIN_Y + turtleRadius(t)
    return t.ycor() < bottom_edge

def isOutRight(t):
    ''' return True if t is outside right-side of Arena, False otherwise '''
    right_edge = ARENA_MAX_X - turtleRadius(t)
    return t.xcor() > right_edge

def isOutLeft(t):
    ''' return True if t is outside left-side of Arena, False otherwise '''
    left_edge = ARENA_MIN_X + turtleRadius(t)
    return t.xcor() < left_edge
    
def isOutOfBounds(t):
    ''' return True if t has moved 'out of bound' (out of arena), False otherwise '''
    return isOutTop(t) or isOutBottom(t) or isOutLeft(t) or isOutRight(t)

def moveIntoBounds(t):
    ''' move t into bounds by at least one turtleRadius '''
    x,y = t.position()
    radius = turtleRadius(t)
    if isOutTop(t):
        y = ARENA_MAX_Y - radius
    if isOutBottom(t):
        y = ARENA_MIN_Y + radius
    if isOutRight(t):
        x = ARENA_MAX_X - radius
    if isOutLeft(t):
        x = ARENA_MIN_X + radius
    t.setposition(x, y)
    
def bounceOffBoundary(t):
    ''' if turtle hits the edge of the playing arena, turn it around '''
    if isOutOfBounds(t):
        t.right(180)
        moveIntoBounds(t)

##### The PLAYER #####

def createPlayer():
    ''' return a turtle representing the player '''
    player = turtle.Turtle()
    player.penup()
    player.speed(0)
    player.color(PLAYER_COLOUR)
    player.shape(PLAYER_SHAPE)
    player.shapesize(PLAYER_SCALE, PLAYER_SCALE)
    return player

def createSnakeSegment():
    ''' return a turtle representing the player '''
    player = turtle.Turtle()
    player.penup()
    player.speed(0)
    player.color('yellow')
    player.shape(PLAYER_SHAPE)
    player.shapesize(PLAYER_SCALE, PLAYER_SCALE)
    return player

# EVENT HANDLING  -- bind key-presses to turtle movement operations.
# Note: Event-driven programming is a challenging concept
#       This code uses some technique not covered in COMP115 - ask if you are interested.
def turnLeft(t):
    ''' turn turtle left one turn unit '''
    t.left(TURN_ANGLE)

def turnRight(t):
    ''' turn turtle right one turn unit '''
    t.right(TURN_ANGLE)

def goForward(t):
    ''' move turtle forward one step, bouncing off Arena boundary if t goes out of bounds '''
    t.forward(STEP_SIZE)
    #bounceOffBoundary(t)

def bindKeyboard(t=None):
    '''
        Bind keyboard events used to control the given turtle.
        Only ONE turtle at a time can be controlled by keyboard events.
        When t==None, keyboard bindings are removed so interactive controls are disabled.
    '''
    from functools import partial

    if t is None:  # remove event bindings
        turtle.onkeypress(None, FORWARD)
        turtle.onkeypress(None, LEFT)
        turtle.onkeypress(None, RIGHT)
    else:  # bind arrow key presses to the turtle motion functions above
        turtle.onkeypress(partial(goForward,t), FORWARD)
        turtle.onkeypress(partial(turnLeft, t), LEFT)
        turtle.onkeypress(partial(turnRight, t), RIGHT)

    turtle.listen()  # give the screen keyboard 'focus'


################################
##### FRAMEWORK UNIT TESTS #####
################################    
def frameworkUnitTests():
    
    # No way to automate tests for these functions -- draw them and check it visually
    drawArenaBoundary()  
    scoreboard = createScoreBoard("These are the instructions displayed on the scoreboard")
    updateScoreBoard(scoreboard, "THIS VALUE SHOULD BE OVERWITTEN")
    updateScoreBoard(scoreboard, "CORRECT TEST SCORE")
    
    # randomeArenaCoordinate
    for i in range(10):
        x, y = randomArenaCoordinate()
        assert x > ARENA_MIN_X and x < ARENA_MAX_X
        assert y > ARENA_MIN_Y and y < ARENA_MAX_Y
    
    t = turtle.Turtle()
    t.penup()
    t.speed(0)
    t.shape('circle')
    
    # turtleRadius
    t.shapesize(0.5, 0.5)
    assert turtleRadius(t) == 0.5 * TURTLE_BODY_SIZE
    t.shapesize(2, 2)
    assert turtleRadius(t) == 2 * TURTLE_BODY_SIZE
    t.shapesize(1, 1)
    assert turtleRadius(t) == TURTLE_BODY_SIZE

    # isOutOfBounds (lower-left)
    t.setposition(ARENA_MIN_X+turtleRadius(t)+1, ARENA_MIN_Y+turtleRadius(t)+1)
    assert not isOutOfBounds(t)
    t.setposition(ARENA_MIN_X+turtleRadius(t)-1, ARENA_MIN_Y+turtleRadius(t)+1)
    assert isOutOfBounds(t)
    t.setposition(ARENA_MIN_X+turtleRadius(t)+1, ARENA_MIN_Y+turtleRadius(t)-1)
    assert isOutOfBounds(t)
    # isOutOfBounds (upper-right)    
    t.setposition(ARENA_MAX_X-turtleRadius(t)-1, ARENA_MAX_Y-turtleRadius(t)-1)
    assert not isOutOfBounds(t)         
    t.setposition(ARENA_MAX_X-turtleRadius(t)+1, ARENA_MAX_Y-turtleRadius(t)-1)
    assert isOutOfBounds(t)         
    t.setposition(ARENA_MAX_X-turtleRadius(t)-1, ARENA_MAX_Y-turtleRadius(t)+1)
    assert isOutOfBounds(t)
    
    # moveIntoBounds
    t.setposition(ARENA_MAX_X+turtleRadius(t), ARENA_MAX_Y+turtleRadius(t))
    assert isOutOfBounds(t)
    moveIntoBounds(t)
    assert not isOutOfBounds(t)

    # bounceOffBoundary
    orig_heading = t.heading()
    t.setposition(ARENA_MAX_X+turtleRadius(t), ARENA_MAX_Y+turtleRadius(t))
    assert isOutOfBounds(t)
    bounceOffBoundary(t)
    assert not isOutOfBounds(t)
    assert t.heading() == (orig_heading + 180)%360

    # createBug / replaceBug
    b = createBug()
    assert not isOutOfBounds(b)
    b = replaceBug(b)
    assert not isOutOfBounds(b)
    
    # randomWalk
    for step in range(1, 5):
        orig_x,orig_y = b.position()
        randomWalk(b, step)
        new_x,new_y = b.position()
        assert abs(orig_x - new_x) <= step
        assert abs(orig_x - new_x) <= step
    
    # isCollision
    b.home()
    b.forward(turtleRadius(b))
    t.home()
    t.shape('arrow')
    t.backward(turtleRadius(t))
    assert not isCollision(t, b)
    t.forward(1)
    assert isCollision(t, b)
    
    removeBug(b)
    removeBug(t)
    
    print("... automated tests completed.")
    print("Interactively test Player controls...")

# Player / Keyboard Events -- no way to automate tests - create player and bind events for interactive testing
    p = createPlayer()
    bindKeyboard(p)
    createTimer('Countdown Timer: ', start_time=42, step=-1)
    turtle.done()
    
    
if __name__ == "__main__":
    print("Running Turtle Game Nano-framework Unit Test suite...")
    frameworkUnitTests()
