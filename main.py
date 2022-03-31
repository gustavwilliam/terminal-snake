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
    while True:
        print(board.render(snake))
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

        # Move cursor to the top left corner of the board
        print(f"\u001b[{board.height}A")
        print(f"\u001b[{board.width}D")

except BaseException as e:  # BaseException, to catch KeyboardInterrupt
    print("\033[?25h", end="")  # Show cursor again
    kb.set_normal_term()
    raise e
