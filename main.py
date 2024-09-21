from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "brown"
FOOD_COLOR = "blue"
BACKGROUND_COLOR = "black"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE, fill =SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0,(GAME_HEIGHT / SPACE_SIZE)-1)*SPACE_SIZE
        check = False
        for body in snake.coordinates:
            if x == body[0] and y == body[1]:
                check = True
        while check:
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            for body in snake.coordinates:
                if x == body[0] and y == body[1]:
                    check = True
            else:
                break

        self.coordinates=[x,y]
        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake,food):
    x,y = snake.coordinates[0]
    if direction == "Up":
        y -= SPACE_SIZE
    elif direction == "Down":
        y += SPACE_SIZE
    elif direction == "Right":
        x += SPACE_SIZE
    elif direction == "Left":
        x -= SPACE_SIZE

    snake.coordinates.insert(0,(x,y))
    square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global SPEED
        score += 1
        if SPEED>60:
            SPEED -= 1
        label.config(text= "Score:{}".format(score))
        canvas.delete("food") #because of the tag
        food = Food() #create new food
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED,next_turn,snake,food)

def change_direction(new_direction):
    global direction
    if new_direction == "Left":
        if direction != "Right":
            direction = new_direction
    if new_direction == "Right":
        if direction != "Left":
            direction = new_direction
    if new_direction == "Up":
        if direction != "Down":
            direction = new_direction
    if new_direction == "Down":
        if direction != "Up":
            direction = new_direction
def check_collisions(snake):
    x,y = snake.coordinates[0]
    if x<0 or x>=GAME_WIDTH:
        print("Game Over")
        return True
    if y<0 or y>= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x==body_part[0] and y==body_part[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font= ("consolas",70), text= "GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Snake Game")
window.resizable(False, False)


score = 0
direction = "Down"
label = Label(window, text="Score:{}".format(score),font = ("consolas",40))
label.pack()

canvas = Canvas(window, bg= BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()


window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<a>",lambda event:change_direction("Left"))
window.bind("<d>",lambda event:change_direction("Right"))
window.bind("<w>",lambda event:change_direction("Up"))
window.bind("<s >",lambda event:change_direction("Down"))
snake = Snake()
food = Food()

next_turn(snake,food)
window.mainloop()


