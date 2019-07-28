import copy, threading, time
from client import DroidClient
from eight_tile_game import EightTileGame

def robot_com(robot_id, heading):
    mapping = {
        "up": 0,
        "right": 90,
        "down": 180,
        "left": 270
    }

    robot = DroidClient()
    ret = robot.connect_to_droid(robot_id)
    while (ret == False):
        ret = robot.connect_to_droid(robot_id)

    if heading != "up":
        robot.roll(0, mapping.get(heading), 0)
        time.sleep(0.3)
    robot.roll(1, mapping.get(heading), 0.65)
    if heading != "up":
        time.sleep(0.3)
        robot.roll(0, 0, 0)

    robot.disconnect()

def start_state(robot_num):
    mapping = {
        1: ("D2-", (0, 0)),
        2: ("D2-", (0, 0)),
        3: ("D2-", (0, 0)),
        4: ("D2-", (0, 0)),
        5: ("D2-", (0, 0)),
        6: ("D2-", (0, 0)),
        7: ("D2-", (0, 0)),
        8: ("D2-", (0, 0))
    }
    return mapping.get(robot_num)

#board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
#game = EightTileGame(board)

robot_com("D2-4663", "up")
robot_com("D2-4663", "down")
robot_com("D2-4663", "left")
robot_com("D2-4663", "right")

#robot_com("Q5-E2A9", "up")
#robot_com("D2-4663", "up")
#robot_com("Q5-E2A9", "up")




'''
# creating threads
thread1 = threading.Thread(target = robot_com, args = (start_state.get(1), "left"))
thread2 = threading.Thread(target = robot_com, args = (start_state.get(2), "right"))
thread1.start()
thread2.start()

# wait until thread 1 is completely executed
thread1.join()
# wait until thread 2 is completely executed
thread2.join()

# both threads completely executed
print("Done!")
'''

