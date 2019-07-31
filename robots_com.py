import copy, threading, time
from client import DroidClient
from eight_puzzle import EightPuzzle

class Robot(object):

    def __init__(self, robot_id):
        self.robot = DroidClient()
        connected = self.robot.connect_to_droid(robot_id)
        while not connected:
            connected = self.robot.connect_to_droid(robot_id)

    def roll(self, heading):
        mapping = {
            "up": 0,
            "right": 90,
            "down": 180,
            "left": 270
        }
        self.robot.roll(0, mapping.get(heading), 0)
        time.sleep(0.35)
        self.robot.roll(1, mapping.get(heading), 0.62)

    def reset(self):
        self.robot.roll(0, 0, 0)

    def disconnect(self):
        self.robot.disconnect()

def get_robot_id(robot_num):
    mapping = {
        1: "Q5-C8A8",
        2: "D2-4663",
        3: "Q5-4F64",
        4: "D2-96AF",
        5: "Q5-DFAA",
        6: "D2-05A0",
        7: "Q5-D26A",
        8: "D2-8675"
    }
    return mapping.get(robot_num)

commands = []
robot_nums = set()
robots = []

while True:
    commands = []
    robot_nums = set()
    robots = [None for i in range(9)]

    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    game = EightPuzzle(board)
    game.scramble(100)

    commands = game.find_soln()
    for command in commands:
        robot_nums.add(command[0])

    print(game.get_board())
    print("# of robots that need to be connected: " + str(len(robot_nums)))
    print("# of moves required: " + str(len(commands)))
    print("Enter s to start or any other key to re-scramble:")
    choice = input()
    if choice == "s":
        break

print("Started")

for i in robot_nums:
    robots[i] = Robot(get_robot_id(i))

print("Enter any key to execute commands:")
input()

for command in commands:
    robots[command[0]].roll(command[1])

for i in robot_nums:
    robots[i].reset()
    robots[i].disconnect()
