from tkinter import *
import random

#constants
GAME_WIDTH = 1350
GAME_HEIGHT = 720
SPEED = 200
SPACE_SIZE  = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"  #GREEN
FOOD_COLOR = "#FF0000" #RED
BACKGROUND_COLOR ="#000000" #BLACK

class Snake:
    def __init__(self):
        
        self.body_size = BODY_PARTS # Initial body size
        self.coordinates = [] # List to store the coordinates of each snake segment
        self.squares = [] # List to store the graphical representation 

        #Creating the initial snake based on BODY_PARTS specified. Will be created at [0,0]
        for i in range (0,BODY_PARTS):
            self.coordinates.append([0,0])

        #drawing the snake
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        
        #generating food at random places
        x = random.randint(0,int(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0,int(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE

        #self.coordinates stores x and y values
        self.coordinates=[x,y]
        #draws snake
        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOR,tag="food")

def next_turn(snake,food):

    #Get current x,y position of snake's head
    x,y = snake.coordinates[0]

    #each move by snake is 50 pixels ie space_size's value
    #update head position based on direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #Up ("up") → Decrease y (move up).
    #Down ("down") → Increase y (move down).
    #Left ("left") → Decrease x (move left).
    #Right ("right") → Increase x (move right).

    snake.coordinates.insert(0,(x,y)) #Insert the New Head Position at the Front

    square = canvas.create_rectangle(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR) #Draw the New Head on the Canvas. New rectangle becomes new head.

    snake.squares.insert(0,square) #Add the New Head to the squares List


    #Check if the Snake Eats the Food
    if x == food.coordinates[0] and y == food.coordinates[1]: #Compares the new head’s x, y with the food’s x, y.
        #If it matches, snake ate the food.

        #Increment the score. Update the score. Delete the food and create new food.
        global score
        score = score + 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    #If food is not eaten
    else:
        del snake.coordinates[-1] #Remove the last segment to maintain the same length.
        canvas.delete(snake.squares[-1])
        del snake.squares[-1] #Deletes the last rectangle from canvas and squares.

    #Check for Collisions
    if check_collisions(snake): #If it collides, the game ends.
        game_over()

    #Schedule the Next Move
    else:
        window.after(SPEED,next_turn,snake,food) #Keeps the game running by repeatedly calling next_turn().


def change_direction(new_direction):
#This function updates the direction in which the snake moves.If the new direction is not opposite to the current direction, update direction.
    global direction #old direction
    
    if new_direction == 'left': #if moving "right", it cannot move "left", otherwise it would collide with itself.
        if direction !='right':
            direction = new_direction

    elif new_direction == 'right':
        if direction !='left':
            direction = new_direction

    elif new_direction == 'up': #If moving "up", it cannot move "down" immediately.
        if direction !='down':
            direction = new_direction

    elif new_direction == 'down':
        if direction !='up':
            direction = new_direction

def check_collisions(snake):
#This function checks if the snake hits the wall or itself.

    x,y = snake.coordinates[0] # Head of the snake

    #Check Wall Collision
    if x <0 or x >= GAME_WIDTH:
        return True  

    elif y <0 or y >= GAME_HEIGHT:
        return True  

    # Check Self-Collision
    for body_part in snake.coordinates[1:]:  #Loops through the entire body (except the head).
        if x == body_part[0] and y == body_part[1]:
            return True #if the head’s (x, y) matches any body part, return True (collision detected).

    return False  #If No Collision, Return False


def game_over():
#This function stops the game and displays "GAME OVER" on the screen.

    canvas.delete(ALL) #Removes all objects (snake, food, score, etc.).
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2, font=('consolas',70),text="GAME OVER", fill="red",tag="gameover")

window = Tk() #Creates a window using Tk().
window.title("Snake Game")
window.resizable(width=False,height=False) #Prevents resizing so that the game screen remains fixed.
window.focus_force() 

score = 0 #Creates a label to display the score.Starts at 0
direction = 'down'

label = Label(window, text="Score:{}".format(score),font=('consolas',40)) #Updates dynamically when the snake eats food.
label.pack()

canvas = Canvas(window,bg=BACKGROUND_COLOR, height=GAME_HEIGHT,width=GAME_WIDTH) #Creates the game area where the snake and food are displayed.
canvas.pack()

#Centering the Window
window.update()  # Update the window to get correct dimensions

#Get the window size & Get screen size.
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()  
screen_height = window.winfo_screenheight()

#Centers the window horizontally & Centers the window vertically.
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Apply positioning & Moves the window to the center.

#Binds arrow keys to the change_direction function ie When left arrow is pressed → change_direction("left") is called.
window.bind('<Left>',lambda event :change_direction('left'))
window.bind('<Right>',lambda event :change_direction('right'))
window.bind('<Up>',lambda event :change_direction('up'))
window.bind('<Down>',lambda event :change_direction('down'))

#Create Snake & Food Objects
snake = Snake() #Creates the Snake object (starts with 3 body parts at [0,0]).
food = Food() #Creates the Food object (random position on the grid).

next_turn(snake,food) #Calls next_turn() to start moving the snake.

window.mainloop()