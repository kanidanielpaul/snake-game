import tkinter
import time
import random

from tkinter import messagebox


class Cell:
    '''
    represents a single block on screen
    '''
    GREY = "grey"
    RED = "red"
    WHITE = "white"
    BLUE = "blue"

    def __init__(self, canvas:tkinter.Canvas, x:int, y:int, size:int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.x1 = self.x * self.size
        self.y1 = self.y * self.size
        self.x2 = self.x1 + self.size
        self.y2 = self.y1 + self.size
        self.id = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=Cell.GREY, outline=Cell.GREY)
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    def reset(self):
        self.set_fill(Cell.GREY)

    def set_fill(self, color:str):
        self.canvas.itemconfig(self.id, fill=color)

    def set_outline(self, color:str):
        self.canvas.itemconfig(self.id, outline=color)


class Snake:
    '''
    represents a single block of the snakes body
    each snake block points to the next block on its body
    '''
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(self, cell:Cell):
        self.cell = cell
        self.direction = None
        self.next = None

    def move(self):
        current_cell = self.cell

        if self.direction == Snake.RIGHT:
            self.cell = current_cell.right
        elif self.direction == Snake.LEFT:
            self.cell = current_cell.left
        elif self.direction == Snake.UP:
            self.cell = current_cell.up
        elif self.direction == Snake.DOWN:
            self.cell = current_cell.down

        # delete existing cell/reset color
        current_cell.reset()
        # draw new snake block/set color
        self.cell.set_fill(Cell.RED)

        # if snake block has another block, recursively call all the above steps on it too until no more blocks
        if self.next is not None:
            self.next.move()
            self.next.direction = self.direction


    def set_direction(self, direction:str):
        '''
        snake cannot go 180 degrees opposite to the direction its currently moving
        '''
        if self.direction == Snake.RIGHT and direction == Snake.LEFT:
            return

        if self.direction == Snake.LEFT and direction == Snake.RIGHT:
            return

        if self.direction == Snake.UP and direction == Snake.DOWN:
            return

        if self.direction == Snake.DOWN and direction == Snake.UP:
            return

        self.direction = direction

    def grow(self):
        if self.next is None:
            self.next = Snake(self.cell)
        else:
            self.next.grow()


class Fruit:
    def __init__(self, cell:Cell):
        self.cell = cell
        self.cell.set_fill(Cell.BLUE)


class SnakeGame(tkinter.Tk):
    def __init__(self, width:int, height:int):
        super().__init__()
        self.width = width
        self.height = height
        self.size = 10

        self.var_score = tkinter.IntVar()
        self.var_score.set(0)

        container = tkinter.Frame(self, highlightthickness=1, highlightbackground="grey")
        container.pack(fill=tkinter.BOTH, expand=True, padx=2, pady=2)

        frame_status = tkinter.Frame(container)
        frame_status.pack(fill=tkinter.X)

        tkinter.Label(frame_status, text="Score:").pack(side=tkinter.LEFT)
        tkinter.Label(frame_status, textvariable=self.var_score).pack(side=tkinter.LEFT)

        self.canvas = tkinter.Canvas(container, width=self.width * self.size, height=self.height * self.size)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)

        self.cells = []

        # create all cells
        for h in range(self.height):
            row = []
            for w in range(self.width):
                cell = Cell(canvas=self.canvas, x=w, y=h, size=self.size)
                row.append(cell)
            self.cells.append(row)

        # set cells left, right, top and bottom cells
        for row_index, row in enumerate(self.cells):
            for cell_index, cell in enumerate(row):
                if cell.x == self.width - 1:
                    cell.right = self.cells[row_index][0]
                else:
                    cell.right = self.cells[row_index][cell_index + 1]

                if cell.x == 0:
                    cell.left = self.cells[row_index][-1]
                else:
                    cell.left = self.cells[row_index][cell_index - 1]

                if cell.y == self.height - 1:
                    cell.down = self.cells[0][cell_index]
                else:
                    cell.down = self.cells[row_index + 1][cell_index]

                if cell.y == 0:
                    cell.up = self.cells[-1][cell_index]
                else:
                    cell.up = self.cells[row_index - 1][cell_index]

        self.snake = Snake(cell=self.cells[random.randrange(1, self.height)][random.randrange(1, self.width)])
        self.fruit = Fruit(cell=self.cells[random.randrange(1, self.height)][random.randrange(1, self.width)])

        self.bind("<Key>", self.key_press)

    def wait(self, secs:float):
        time.sleep(secs)

    def set_title(self, title:str):
        self.title(title)

    def set_resizable(self, value:bool):
        self.resizable(value, value)

    def key_press(self, event):
        if event.keysym == "Up":
            self.snake.set_direction(Snake.UP)
        elif event.keysym == "Down":
            self.snake.set_direction(Snake.DOWN)
        elif event.keysym == "Left":
            self.snake.set_direction(Snake.LEFT)
        elif event.keysym == "Right":
            self.snake.set_direction(Snake.RIGHT)

    def snake_bite_itself(self):
        '''
        checks if snake bit itself
        '''
        next_snake = self.snake.next

        while next_snake is not None:
            if self.snake.cell.x == next_snake.cell.x and self.snake.cell.y == next_snake.cell.y:
                return True

            next_snake = next_snake.next

        return False

    def snake_ate_fruit(self):
        '''
        checks if the snake ate the fruit
        '''
        return self.snake.cell.x == self.fruit.cell.x and self.snake.cell.y == self.fruit.cell.y

    def randomize_fruit(self):
        self.fruit.cell.reset()
        self.fruit = Fruit(cell=self.cells[random.randrange(1, self.height)][random.randrange(1, self.width)])

    def increment_score(self):
        self.var_score.set(self.var_score.get() + 1)

    def show_message(self, message:str):
        messagebox.showinfo(title="Info", message=message)


def main():
    game = SnakeGame(width=50, height=50)
    game.set_title(title="Snake v0.1")
    game.set_resizable(False)

    while True:
        game.snake.move()

        if game.snake_bite_itself():
            game.show_message("Game Over")
            break

        if game.snake_ate_fruit():
            game.increment_score()
            game.randomize_fruit()
            game.snake.grow()

        game.update()
        game.wait(secs=0.05)


if __name__ == "__main__":
    main()
