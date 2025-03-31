from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range (0, BODY_PARTS):
            self.coordinates.append([0, 0])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.squares.append(square)
            
class Food:
    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill = FOOD_COLOR, tag = "food")    


def nextTurn(snake, food):
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    snake.coordinates.insert(0, (x, y))
    
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        
        score += 1
        
        label.config(text = f"Score:{score}")
        
        canvas.delete("food") # we can use "food" because we have given it a tag
        
        food = Food() # create new food
    else:
        del snake.coordinates[-1] # last set of coordinates
    
        canvas.delete(snake.squares[-1]) # delete last square
    
        del snake.squares[-1] # delete last square from list
        
    if checkCollisions(snake):
        gameOver()
        
    else:
        window.after(SPEED, nextTurn, snake, food)

def changeDirection(newDirection):
    global direction
    
    if newDirection == 'left':
        if direction != 'right':
            direction = newDirection
    elif newDirection == 'right':
        if direction != 'left':
            direction = newDirection
    if newDirection == 'up':
        if direction != 'down':
            direction = newDirection
    if newDirection == 'down':
        if direction != 'up':
            direction = newDirection
    

def checkCollisions(snake):
    x, y = snake.coordinates[0]
    
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for bodyPart in snake.coordinates[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            return True
        
    return False

def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font = ('consolas', 70), text = "Game Over", fill = "red", tag = "gameover")
    

window = Tk()
window.title("Snake Game")  
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text = f"Score: {score}", font = ("consolas", 40))
label.pack()

canvas = Canvas(window, bg = BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()

# centering the window when it appears
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()  
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: changeDirection('left'))
window.bind('<Right>', lambda event: changeDirection('right'))
window.bind('<Up>', lambda event: changeDirection('up'))
window.bind('<Down>', lambda event: changeDirection('down'))

snake = Snake()
food = Food()

nextTurn(snake, food)

window.mainloop()