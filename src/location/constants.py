import enum

class GameStatus(enum.Enum):
    STARTING = 'starting'
    IN_PROGRESS = 'in_progress'
    FINISHED = "finished"

class TaskStatus(enum.Enum):
    RUNNING = 'running'
    FINISHED = "finished"

GAME_BOARD = {
    1:None,
    2:None,
    3:None,
    4:None,
    5:None,
    6:None,
    7:None,
    8:None,
    9:None,
}