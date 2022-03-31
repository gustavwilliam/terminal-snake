from models import Board, Snake, Objects, Directions
from keyboard import KBHit
import time


DIRECTION_MAP = {
    0: Directions.UP,
    1: Directions.RIGHT,
    2: Directions.DOWN,
    3: Directions.LEFT,
}

kb = KBHit()
print("\033[?25l", end="")  # Hide cursor

board = Board(50, 18)
snake = Snake()
board.board[snake.position[0]][snake.position[1]] = Objects.SNAKE
board.place_apple()

try:
    print(end='\033[H\033[m\033[2J', flush=True)  # Clear screen

    while True:
        print('\033[H', end=board.render(snake), flush=True)

        time.sleep(0.1)

        if kb.kbhit():
            direction = DIRECTION_MAP[kb.getarrow()]
            if tuple(x + y for x, y in zip(direction.value, snake.direction.value)) != (
                0,
                0,
            ):
                snake.direction = (
                    direction  # ^ Make sure that we don't turn around 180° in one turn
                )

        snake.move(board)

finally:
    print("\033[?25h", end="")  # Show cursor again
    kb.set_normal_term()
    print(flush=True)  # Send out newline