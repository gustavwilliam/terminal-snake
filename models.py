from dataclasses import dataclass
import random

from enum import Enum
from itertools import product
from queue import Queue


class Directions(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)


class Objects(Enum):
    SNAKE = "██"
    APPLE = "╣╠"
    EMPTY = "  "


snakeheads = {
    "RIGHT": "█▙",
    "LEFT": "▟█",
    "UP": "▟▙",
    "DOWN": "▜▛",
}


@dataclass
class RenderSettings:
    texture: str = "▒"  # Single character
    enclose_game: bool = True
    show_score: bool = True


class Board:
    def __init__(
        self,
        width: int,
        height: int,
        render_settings: RenderSettings = RenderSettings(),
    ):
        self.width = width
        self.height = height
        self.board_width = self.width // 2 - 1
        self.board_height = self.height

        if render_settings.enclose_game:
            self.board_width -= 1
            self.board_height -= 4
        if render_settings.show_score:
            self.board_height -= 4

        self.render_settings = render_settings
        self.coordinates = product(range(self.board_height), range(self.board_width))
        self.board = [
            [Objects.EMPTY for _ in range(self.board_width)]
            for _ in range(self.board_height)
        ]

    def empty_coordinates(self) -> list[tuple[int, int]]:
        coordinates = product(range(self.board_height), range(self.board_width))
        return [(x, y) for x, y in coordinates if self.board[x][y] == Objects.EMPTY]

    def place_apple(self):
        x, y = random.choice(self.empty_coordinates())
        self.board[x][y] = Objects.APPLE

    @staticmethod
    def replace_head(
        element: Objects, position: tuple[int, int], snake: "Snake"
    ) -> str:
        if element.name == "SNAKE":
            if position == snake.position:
                return snakeheads[snake.direction.name]
        return element.value

    def render(self, snake: "Snake") -> str:
        rows = []

        if self.render_settings.show_score:
            if self.render_settings.enclose_game:
                rows.append(self.render_settings.texture * self.width)
                if self.board_width * 2 >= 12:
                    rows.append(
                        self.render_settings.texture * 2
                        + f" SCORE: {snake.length}"
                        + " " * (self.width - 12 - len(str(snake.length)))
                        + self.render_settings.texture * 2
                    )
                else:
                    rows.append(
                        self.render_settings.texture * 2
                        + str(snake.length)
                        + self.render_settings.texture * 2
                    )
            else:
                rows.append(
                    f" SCORE: {snake.length}" if self.width >= 12 else str(snake.length)
                )
                rows.append("┏" + "━" * (self.board_width * 2 - 1))

        if self.render_settings.enclose_game:
            rows.append(self.render_settings.texture * self.width)

        for i, row in enumerate(self.board):
            row_list = []

            if self.render_settings.enclose_game:
                row_list = [element for element in reversed(row)]
            else:
                inlcude_blanks = False
                for element in reversed(row):
                    if element == Objects.EMPTY and inlcude_blanks:
                        row_list.append(element)
                    elif element != Objects.EMPTY:
                        row_list.append(element)
                        inlcude_blanks = True

            board_row = "".join(
                self.replace_head(x, (i, j), snake)
                for j, x in enumerate(reversed(row_list))
            )
            if self.render_settings.enclose_game:
                rows.append(
                    self.render_settings.texture * 2
                    + board_row
                    + self.render_settings.texture * 2
                )
            else:
                rows.append("┃" + board_row)

        if self.render_settings.enclose_game:
            rows.append(self.render_settings.texture * self.width)

        return "\n".join(rows)


class Snake:
    def __init__(
        self,
        direction: Directions = Directions.RIGHT,
        position: tuple[int, int] = (0, 0),
        teleport_through_walls: bool = True,
    ):
        self.direction = direction
        self.position = position
        self.teleport_through_walls = teleport_through_walls
        self.length = 1
        self.queue = Queue()
        self.queue.put(self.position)  # Add the starting position

    def next_position(self):
        return (
            self.position[0] + self.direction.value[0],
            self.position[1] + self.direction.value[1],
        )

    def move(self, board: Board):
        x, y = self.next_position()

        if self.teleport_through_walls:
            if x < 0:
                x = board.board_height - 1
            elif x >= board.board_height:
                x = 0
            if y < 0:
                y = board.board_width - 1
            elif y >= board.board_width:
                y = 0
        else:
            if x < 0 or x >= board.board_height or y < 0 or y >= board.board_width:
                raise ValueError("Snake has hit the wall")

        self.position = x, y
        current_type = board.board[x][y]

        self.queue.put((x, y))
        board.board[x][y] = Objects.SNAKE

        if current_type == Objects.SNAKE:
            exit()
        elif current_type == Objects.APPLE:
            self.length += 1
            board.place_apple()
        else:
            r_x, r_y = self.queue.get()
            board.board[r_x][r_y] = Objects.EMPTY  # Remove last part of the tail
