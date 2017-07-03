import discord
import variables
import math
class Bet:
    wagers = []
    name = ""
    side1 = ""
    side1Total = 0
    side2 = ""
    side2Total = 0
    total = 0
    closed = False
    def __init__(self, name, side1, side2):
        self.name = name
        self.side1 = side1
        self.side2 = side2

    def __str__(self):
        if self.closed:
            string = "Closed"
        else:
            string = "Open"
        return self.name + ", " + self.side1 + " - " + str(self.side1Total) + ", " + self.side2 + " - " + str(self.side2Total) + ", Total - " + str(self.total) + ". Bet is " + string + "."
    def makeWager(self, user, side, amount):
        if amount < 1:
            return None
        wager = Wager(user, side, amount, self)
        print(wager)
        print(side)
        print(self.side1)
        print(self.side2)
        if side.strip().lower() == self.side1.strip().lower():
            self.side1Total += amount
            self.total += amount
            self.wagers.append(wager)
            for w in self.wagers:
                w.bet = self
            return wager
        elif side.strip().lower() == self.side2.strip().lower():
            self.side2Total += amount
            self.total += amount
            self.wagers.append(wager)
            for w in self.wagers:
                w.bet = self
            return wager
        return None
    def payout(self, side):
        results = []
        if side.strip().lower() == self.side1.strip().lower():
            wTotal = self.side1Total
            lTotal = self.side2Total
        elif side.strip().lower() == self.side2.strip().lower():
            wTotal = self.side2Total
            lTotal = self.side1Total
        else:
            return None
        if self.side1Total is self.total or self.side2Total is self.total:
            return results
        for wager in self.wagers:
            if wager.side.strip().lower() == side.strip().lower():
                results.append((wager.user, True, math.ceil     (wager.amount/wTotal) * lTotal))
            else:
                results.append((wager.user, False, wager.amount))
        return results
    def delete(self):
        print(self)
        for wager in self.wagers:
            user = wager.user
            usersW = variables.wagers[user]
            #print(usersW)
            usersW.remove(wager)
            variables.wagers[user] = usersW
    def close(self):
        self.closed = not self.closed
        return self.closed
class Wager:
    def __init__(self, user, side, amount, bet):
        self.user = user
        self.amount = amount
        self.side = side
        self.bet = bet

    def __str__(self):
        return str(self.amount) + " on " + self.side + " for the bet " + self.bet.name + ". Currently set to win " + str(self.calculatePayout()) + "."
    def calculatePayout(self):
        side1 = self.bet.side1
        try:
            if self.side.strip().lower() == side1.strip().strip():
                print(self.bet.side1Total)
                return math.ceil(self.amount/self.bet.side1Total) * self.bet.side2Total
            else:
                print(self.bet.side2Total)
                return math.ceil(self.amount /self.bet.side2Total) * self.bet.side1Total
        except Exception: #divide by zero
            return 0