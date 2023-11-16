#!/bin/python

"""
supports single rolls of "XdY" + constant
 3d4 - 2
 6d10000
 4d7p + 3
"""

import random
import re
from twitchio.ext import commands

class Roller:
    def __init__(self):
        self.numPens = 0
        self.total = 0
        self.isPenetrating = False
        self.resultStr = ""
        self.response = ""

    def refresh(self):
        self.numPens = 0
        self.total = 0
        self.isPenetrating = False
        self.resultStr = ""

    def rollPen(self, faces, sign):
        decrStr = "-1"
        if sign < 0:
            decrStr = "+1"
        result = sign*random.randrange(1, faces + 1, 1)
        self.resultStr += ", pen[" + str(result) + decrStr + "]"
        self.total += result + -1*sign*1
        if abs(result) == faces:
            self.numPens += 1
            self.rollPen(faces, sign)

    def roll(self, rolls, faces, sign=1):
        for i in range(rolls):
            result = sign*random.randrange(1, faces + 1, 1)
            self.resultStr += str(result)
            self.total += result
            if self.isPenetrating and abs(result) == faces:
                self.numPens += 1
                self.rollPen(faces, sign)
            if i < rolls-1:
                self.resultStr += ", "
        self.response += self.resultStr + " "
        self.response += "(sum: " + str(self.total) + ") "

    def rollTermString(self, dieString):
        if "--" in dieString:
            self.response += "Warning: Replacing -- with +. "
            dieString = dieString.replace("--", "+")
        if "++" in dieString:
            self.response += "Warning: ++ found in roll request. "
            dieString = re.sub("\++", "+", dieString)
        if "-+" in dieString:
            self.response += "Warning: -+ found in roll request. "
            dieString = re.sub("-\+", "-", dieString)

        if dieString == "":
            self.response = "no die string"
            return

        dieString = dieString.replace("-", "+-") #hack to delimit subractions and fix leading negative signs
        if dieString[0:2] == "+-": ###############
            dieString = dieString[1:] ############

        dieString = dieString.strip().lower().replace(" ", "")
        terms = re.split("\+", dieString) 
        totalSum = 0
        totalPens = 0
        for term in terms:
            self.refresh()
            self.rollDieTerm(term)
            totalSum += self.total
            totalPens += self.numPens
        self.response += "Total Pens: " + str(totalPens) + ". "
        self.response += "Total Sum: " + str(totalSum) + "."

    def rollDieTerm(self, dieTerm):
        sign = 1
        badConditions = [
            dieTerm[-1] == "d",
            "d1p" in dieTerm,
            dieTerm == "-",
            dieTerm == ""
        ]
        if True in badConditions:
            self.response = "!!Bad die term!!: " + dieTerm + " " 
            return
        if dieTerm[0] == "-":
            sign = -1
            dieTerm = dieTerm[1:]
        signChar = "+"
        signPref = ""
        if sign < 0:
            signChar = "-"
            signPref = "-"
        digitMatch = re.match("^\d+$", dieTerm)
        termIsConstant = False
        if digitMatch != None:
            termIsConstant = dieTerm == digitMatch.group(0)
        if termIsConstant:
            self.response += signChar + dieTerm + " "
            self.total += sign*int(dieTerm)
            return
        if dieTerm[0] == "d":
            dieTerm = "1" + dieTerm
        parts = re.split("[d]\s*", dieTerm)
        numberOfRolls = int(parts[0])
        numberOfFaces = int(parts[1].replace("p",""))
        self.isPenetrating = "p" in parts[1]
        self.response += "*roll " + signPref + parts[0] + "d" + parts[1] + "*: "
        self.roll(numberOfRolls, numberOfFaces, sign)


TOKEN="TWITCH_TOKEN"

class ProllBot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, prefix='!', initial_channels=[""])
    async def event_ready(self):
        print (f"logged in as | {self.nick}")
    @commands.command()
    async def roll(self, ctx: commands.Context, *,  dieString: str) -> None:
        if dieString.strip().replace(" ", "") != "":
            roller = Roller()
            roller.rollTermString(dieString)
            await ctx.send(ctx.author.name + ": " + roller.response)


prollbot = ProllBot()
prollbot.run()
