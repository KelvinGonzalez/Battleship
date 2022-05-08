import random
import os

size = 10
emptySign = "."

letterToIndex = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
signs = {(True, True): "X", (True, False): "+", (False, True): "O", (False, False): "."}
incognetoSigns = {(True, True): "X", (True, False): "+", (False, True): ".", (False, False): "."}

def parsePosition(position):
    return (int(position[1:]) - 1, letterToIndex[position[0]])

class BattleShip:
    def __init__(self, name, size, positions=None):
        if positions is None:
            positions = []
        self.name = name
        self.size = size
        self.positions = positions

    def addPosition(self, position):
        self.positions.append(position)

    def hasPosition(self, position):
        return position in self.positions

    def wasSunk(self, player):
        for position in self.positions:
            if not player.board[position[0]][position[1]]:
                return False
        return True

class Player:
    def __init__(self, name, ships=None):
        if ships is None:
            ships = []
        self.name = name
        self.board = []
        self.ships = ships
        for i in range(size):
            row = []
            for j in range(size):
                row.append(False)
            self.board.append(row)

    def findShip(self, position):
        for ship in self.ships:
            if ship.hasPosition(position):
                return ship
        return None

    def shipInPosition(self, position):
        return self.findShip(position) is not None

    def allShipsSunk(self):
        for ship in self.ships:
            if not ship.wasSunk(self):
                return False
        return True

    def printBoard(self):
        s = self.name + " Board\n"
        for i in range(size):
            ps = ""
            for j in range(size):
                ps += signs[(self.board[i][j], self.shipInPosition((i, j)))] + " "
            s += ps + " " + str(i + 1) + "\n"
        s += "A B C D E F G H I J\n"
        print(s)

    def addShipPositions(self, position, direction, battleShip):
        if direction == "U":
            tempPositions = []
            j = position[1]
            if j < 0 or j >= size:
                return False
            for i in range(position[0] - battleShip.size + 1, position[0] + 1):
                if i < 0 or i >= size:
                    return False
                if self.shipInPosition((i, j)):
                    return False
                tempPositions.append((i, j))
            battleShip.positions = tempPositions

        elif direction == "D":
            tempPositions = []
            j = position[1]
            if j < 0 or j >= size:
                return False
            for i in range(position[0], position[0] + battleShip.size):
                if i < 0 or i >= size:
                    return False
                if self.shipInPosition((i, j)):
                    return False
                tempPositions.append((i, j))
            battleShip.positions = tempPositions

        elif direction == "L":
            tempPositions = []
            i = position[0]
            if i < 0 or i >= size:
                return False
            for j in range(position[1] - battleShip.size + 1, position[1] + 1):
                if j < 0 or j >= size:
                    return False
                if self.shipInPosition((i, j)):
                    return False
                tempPositions.append((i, j))
            battleShip.positions = tempPositions

        else:
            tempPositions = []
            i = position[0]
            if i < 0 or i >= size:
                return False
            for j in range(position[1], position[1] + battleShip.size):
                if j < 0 or j >= size:
                    return False
                if self.shipInPosition((i, j)):
                    return False
                tempPositions.append((i, j))
            battleShip.positions = tempPositions

        return True

    def attack(self, position):
        self.board[position[0]][position[1]] = True
        ship = self.findShip(position)
        if ship is None:
            print(f"Attack on {self.name} missed!\n")
            return False
        print(f"Attack on {self.name} hit!")
        if ship.wasSunk(self):
            print(f"{self.name}'s {ship.name} was sunk!")
        print()


def printBoards():
    s = "Player Board\t\tCPU Board\n"
    for i in range(size):
        ps = ""
        cs = ""
        for j in range(size):
            ps += signs[(player.board[i][j], player.shipInPosition((i, j)))] + " "
            cs += incognetoSigns[(cpu.board[i][j], cpu.shipInPosition((i, j)))] + " "
        s += ps + "\t" + cs + " " + str(i+1) + "\n"
    s += "A B C D E F G H I J\tA B C D E F G H I J\n"
    print(s)


player = Player("Player", [BattleShip("Destroyer", 2), BattleShip("Cruiser", 3), BattleShip("Submarine", 3), BattleShip("Battleship", 4), BattleShip("Carrier", 5)])
cpu = Player("CPU", [BattleShip("Destroyer", 2), BattleShip("Cruiser", 3), BattleShip("Submarine", 3), BattleShip("Battleship", 4), BattleShip("Carrier", 5)])


def cpuAttack():
    def getHitPosition():
        for i in range(size):
            for j in range(size):
                ship = player.findShip((i, j))
                if player.board[i][j] and ship is not None and not ship.wasSunk(player):
                    return (i, j)
        return None

    position = getHitPosition()
    if position is None:
        while True:
            attackPosition = (random.randint(0, size - 1), random.randint(0, size - 1))
            if not player.board[attackPosition[0]][attackPosition[1]]:
                player.attack(attackPosition)
                return
    else:
        if position[0]-1 >= 0 and position[0]-1 < size and player.board[position[0]-1][position[1]] and player.shipInPosition((position[0]-1, position[1])) and not player.findShip((position[0]-1, position[1])).wasSunk(player):
            i = position[0]-1
            while player.board[i][position[1]]:
                i -= 1
                if i < 0 or i >= size or (player.board[i][position[1]] and not player.shipInPosition((i, position[1]))):
                    player.attack((position[0]+1, position[1]))
                    return
            if not player.board[position[0]+1][position[1]]:
                player.attack(random.choice([(position[0]+1, position[1]), (i, position[1])]))
            else:
                player.attack((i, position[1]))

        elif position[0]+1 >= 0 and position[0]+1 < size and player.board[position[0]+1][position[1]] and player.shipInPosition((position[0]+1, position[1])) and not player.findShip((position[0]+1, position[1])).wasSunk(player):
            i = position[0]+1
            while player.board[i][position[1]]:
                i += 1
                if i < 0 or i >= size or (player.board[i][position[1]] and not player.shipInPosition((i, position[1]))):
                    player.attack((position[0]-1, position[1]))
                    return
            if not player.board[position[0]-1][position[1]]:
                player.attack(random.choice([(position[0]-1, position[1]), (i, position[1])]))
            else:
                player.attack((i, position[1]))

        elif position[1]-1 >= 0 and position[1]-1 < size and player.board[position[0]][position[1]-1] and player.shipInPosition((position[0], position[1]-1)) and not player.findShip((position[0], position[1]-1)).wasSunk(player):
            j = position[1]-1
            while player.board[position[0]][j]:
                j -= 1
                if j < 0 or j >= size or (player.board[position[0]][j] and not player.shipInPosition((position[0], j))):
                    player.attack((position[0], position[1]+1))
                    return
            if not player.board[position[0]][position[1]+1]:
                player.attack(random.choice([(position[0], position[1]+1), (position[0], j)]))
            else:
                player.attack((position[0], j))

        elif position[1]+1 >= 0 and position[1]+1 < size and player.board[position[0]][position[1]+1] and player.shipInPosition((position[0], position[1]+1)) and not player.findShip((position[0], position[1]+1)).wasSunk(player):
            j = position[1]+1
            while player.board[position[0]][j]:
                j += 1
                if j < 0 or j >= size or (player.board[position[0]][j] and not player.shipInPosition((position[0], j))):
                    player.attack((position[0], position[1]-1))
                    return
            if not player.board[position[0]][position[1]-1]:
                player.attack(random.choice([(position[0], position[1]-1), (position[0], j)]))
            else:
                player.attack((position[0], j))

        else:
            while True:
                attackPosition = random.choice([(position[0]-1, position[1]), (position[0]+1, position[1]), (position[0], position[1]-1), (position[0], position[1]+1)])
                if not player.board[attackPosition[0]][attackPosition[1]]:
                    break
            player.attack(attackPosition)


for ship in player.ships:
    player.printBoard()
    while True:
        try:
            position = input(f"Input coordinate to place your {ship.name} (Size: {ship.size}): ")
            direction = input(f"Input direction to face your {ship.name} (Size: {ship.size}): ")
            if player.addShipPositions(parsePosition(position), direction, ship):
                print("Ship successfully placed.")
                os.system("cls")
                break
            print("Invalid ship position")
        except:
            print("Good one, you broke something! :/")

for ship in cpu.ships:
    while not cpu.addShipPositions((random.randint(0, size-1), random.randint(0, size-1)), random.choice(["U", "D", "L", "R"]), ship):
        continue

turn = True
while True:
    try:
        if turn:
            printBoards()
            while True:
                position = parsePosition(input("Enter position to attack: "))
                if not cpu.board[position[0]][position[1]]:
                    break
                print("That position has already been attacked.")
            os.system("cls")
            cpu.attack(position)
            if cpu.allShipsSunk():
                printBoards()
                print("Player wins!")
                break
        else:
            cpuAttack()
            if player.allShipsSunk():
                printBoards()
                print("CPU wins!")
                break
        turn = not turn
    except:
        os.system("cls")
        print("Bruh, use an actual move this time. :|\n")

input()
