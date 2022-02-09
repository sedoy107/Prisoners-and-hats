import random, sys

class Hat:
    RED = True
    BLUE = False
    MAPPING = {RED: "RED", BLUE: "BLUE"}

    @staticmethod
    def getColorAtRandom():
        return random.choice((Hat.RED, Hat.BLUE))

class Prisoner:

    totalCount = 0

    def __init__(self, next):
        self.id = Prisoner.totalCount
        Prisoner.totalCount += 1
        self.next = next
        self.answer = None
        self.hatColor = Hat.getColorAtRandom()
        self.isAlive = True

    def giveAnswer(self, prevAnswer):
        # every first prisoner is a savior
        saviorFlag = (self.id + 1) % 2

        # Not the first prisoner
        if self.next:
            # Last prisoner: answers with the color of the next prisoner
            if prevAnswer is None:
                print("Tail prisoner is being asked.")
                self.answer = self.next.hatColor
            # Somewhere in the middle: returns the answer provided by the previous prisoner
            else:
                if saviorFlag:
                    self.answer = self.next.hatColor
                else:
                    self.answer = prevAnswer
        # The very first prisoner: returns the answer provided by the previous prisoner
        else:
            print("Head prisoner is being asked.")
            self.answer = prevAnswer

    def giveAnswerAlwaysRed(self, prevAnswer):
        self.answer = Hat.RED

    def giveAnswerAlwaysBlue(self, prevAnswer):
        self.answer = Hat.BLUE

    def giveAnswerRandom(self, prevAnswer):
        self.answer = Hat.getColorAtRandom()



class Problem:

    description = '''Задача:
    Сто заключенных выстраивают в колонну и на всех надевают шапки: красного или синего цветов. Количество синих и красных шапок неизвестно. Каждый арестант видит только шапку впереди стоящего человека. Начиная с конца колонны, надзиратель спрашивает у каждого цвет его колпака, и если заключенный прав, то его отпускают, а если нет — казнят. При этом каждый следующий узник слышит ответ предыдущего, но не знает, правильным он оказался или нет.
    О чем нужно договориться заключенным перед испытанием, чтобы на свободе оказалось как можно больше людей?
    '''

    @staticmethod
    def printDescription():
        print(Problem.description)

    def __init__(self, totalPrisoners):
        self.totalPrisoners = totalPrisoners
        self.lastPrisoner = None
        for p in range(0,totalPrisoners):
            if p == 0:
                self.lastPrisoner = Prisoner(None)
            else:
                self.lastPrisoner = Prisoner(self.lastPrisoner)

    def printInfo(self):
        print("Current playout information:")

        currentPrisoner = self.lastPrisoner
        reds = 0
        killed = 0

        while(True):
            if currentPrisoner.hatColor:
                reds += 1
            if not currentPrisoner.isAlive:
                killed += 1
            print(f"Prisoner {currentPrisoner.id}: Hat Color: {Hat.MAPPING[currentPrisoner.hatColor]}")
            currentPrisoner = currentPrisoner.next
            if not currentPrisoner:
                break

        print(f"Total prisonsers: {self.totalPrisoners}")
        print(f"Total prisonsers with RED hat: {reds}")
        print(f"Total prisonsers with BLUE hat: {self.totalPrisoners - reds}")
        print(f"Total prisonsers killed: {killed}")
        print(f"Total prisonsers alive: {self.totalPrisoners - killed}")
        print(f"Kill/Total ratio: {round(float(killed) / self.totalPrisoners, 2) * 100}%")

    def play(self):
        print("Starting the game")

        currentPrisoner = self.lastPrisoner
        prevAnswer = None

        while(True):
            #currentPrisoner.giveAnswer(prevAnswer)
            currentPrisoner.giveAnswer(prevAnswer)
            #currentPrisoner.giveAnswerRandom(prevAnswer)
            #currentPrisoner.giveAnswerAlwaysBlue(prevAnswer)
            #currentPrisoner.giveAnswerAlwaysRed(prevAnswer)
            msg = f"Prisoner {currentPrisoner.id} answers {Hat.MAPPING[currentPrisoner.answer]} and "
            if currentPrisoner.answer != currentPrisoner.hatColor:
                currentPrisoner.isAlive = False
                msg += "getting killed"
            else:
                msg += "survives"

            print(msg)

            prevAnswer = currentPrisoner.answer
            currentPrisoner = currentPrisoner.next
            if not currentPrisoner:
                print("Reached end of prisoner's death line")
                break


Problem.printDescription()
problem = Problem(100)
problem.printInfo()
print("")
problem.play()
print("")
problem.printInfo()
