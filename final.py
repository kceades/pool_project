#Caleb Eades and Christian Guerrero
#CS 5 Black
#VPool
#Final Project

from visual import *
import math
import random
import time

class Board:
    def __init__(self):
        '''constructor for our board class'''
        surface = box(pos = (0.0, -2.5, 0.0), length = 120, width = 70, height = 5, color = (0, 0.5, 0))
        edge1 = box(pos = (0.0, 1.25, 30.0), length = 120, width = 10, height = 2.5, color = (0.35, 0.25, 0))
        edge2 = box(pos = (0.0, 1.25, -30.0), length = 120, width = 10, height = 2.5, color = (0.35, 0.25, 0))
        edge3 = box(pos = (55.0, 1.25, 0.0), axis = (0, 0, 1), length = 50, width = 10, height = 2.5, color = (0.35, 0.25, 0))
        edge4 = box(pos = (-55.0, 1.25, 0.0), axis = (0, 0, 1), length = 50, width = 10, height = 2.5, color = (0.35, 0.25, 0))
        pocket1 = cone(pos = (-50, 0.01, -25), axis = (0, -1, 0), radius = 6, color = color.black)
        pocket2 = cone(pos = (-50, 0.01, 25), axis = (0, -1, 0), radius = 6, color = color.black)
        pocket3 = cone(pos = (0, 0.01, -25), axis = (0, -1, 0), radius = 4.24, color = color.black)
        pocket4 = cone(pos = (0, 0.01, 25), axis = (0, -1, 0), radius = 4.24, color = color.black)
        pocket5 = cone(pos = (50, 0.01, -25), axis = (0, -1, 0), radius = 6, color = color.black)
        pocket6 = cone(pos = (50, 0.01, 25), axis = (0, -1, 0), radius = 6, color = color.black)
        leg1 = cylinder(pos = (50, -5, 25), axis = (0, -10, 0), radius = 5, color = (0.35, 0.25, 0))
        leg2 = cylinder(pos = (50, -5, -25), axis = (0, -10, 0), radius = 5, color = (0.35, 0.25, 0))
        leg3 = cylinder(pos = (-50, -5, 25), axis = (0, -10, 0), radius = 5, color = (0.35, 0.25, 0))
        leg4 = cylinder(pos = (-50, -5, -25), axis = (0, -10, 0), radius = 5, color = (0.35, 0.25, 0))

        self.edges = [edge1, edge2, edge3, edge4]
        self.legs = [leg1, leg2, leg3, leg4]
        self.surface = surface
        self.pockets = [pocket1, pocket2, pocket3, pocket4, pocket5, pocket6]

        self.dots = []
        for i in range(3):
            self.dots += [cone(pos = (-55.0, 2.51, -12.5 + 12.5*i), axis = (0, -1, 0), radius = 1, color = color.white)]
            self.dots += [cone(pos = (55.0, 2.51, -12.5 + 12.5*i), axis = (0, -1, 0), radius = 1, color = color.white)]
        for i in range(3):
            self.dots += [cone(pos = (-37.5 + 12.5*i, 2.51, -30.0), axis = (0, -1, 0), radius = 1, color = color.white)]
            self.dots += [cone(pos = (-37.5 + 12.5*i, 2.51, 30.0), axis = (0, -1, 0), radius = 1, color = color.white)]
            self.dots += [cone(pos = (37.5 - 12.5*i, 2.51, -30.0), axis = (0, -1, 0), radius = 1, color = color.white)]
            self.dots += [cone(pos = (37.5 - 12.5*i, 2.51, 30.0), axis = (0, -1, 0), radius = 1, color = color.white)]

        self.balls = []
        for i in range(1, 6):
            for j in range(i):
                bColor = color.red
                if i == 3 and j == 1:
                    bColor = (0.1, 0.1, 0.1)
                elif i % 2 == 1 and j % 2 == 0:
                    bColor = color.red
                elif i == 4 and j == 1:
                    bColor = color.red
                else:
                    bColor = color.blue
                self.balls += [sphere(pos = vector(-24.0 - 2.6*(i - 1), 1.5, 0.0 - 1.5*(i - 1) + 3.0*j), radius = 1.5, color = bColor)]
        self.balls += [sphere(pos = vector(31.25, 1.5, 0), radius = 1.5, color = color.white)]

        self.cue = cylinder(pos = self.balls[15].pos + vector(1.5, 0.5, 0.0), axis = (40, 10, 0), radius = .5, color = (0.55, 0.45, 0))

        self.headings = []
        for i in range(15):
            self.headings += [vector(0.0, 0.0, 0.0)]
        self.headings += [vector(-1.0, 0.0, 0.0)]
        self.headings += [vector(-0.8, -0.2, 0.0)]

    def eightLeft(self):
        '''Checks to see if the eight ball is the last ball'''
        redOut = 0
        blueOut = 0
        eightOut = False
        for i in range(15):
            if self.balls[i].pos.y < -2.0:
                if i in [0, 3, 5, 7, 10, 12, 14]:
                    redOut += 1
                elif i == 4:
                    eightOut = True
                else:
                    blueOut += 1
        
        if redOut == 7:
            if eightOut == True:
                return 0
            else:
                return 1
        
        elif blueOut == 7:
            if eightOut == True:
                return 2
            else:
                return 3
        
        else:
            if eightOut == True:
                return 4
            else:
                return 5

    def winsFor(self, color, eightStatus):
        '''checks to see if either player has won and prints the winner's name'''
        if eightStatus == 0:
            print "Red wins!"
            return False
        elif eightStatus == 2:
            print "Blue wins!"
            return False
        elif eightStatus == 4:
            print color + " loses. Too bad!"
            return False
        else:
            return True

    def wallCollision(self):
        '''checks to see if any ball has touched the edges and makes them bounce off
        at an angle of reflection equal to the angle of incidence'''
        for i in range(16):
            if self.balls[i].pos.z > (self.edges[0].pos.z - 6.5):
                self.headings[i].z *= -1.0
            elif self.balls[i].pos.z < (self.edges[1].pos.z + 6.5):
                self.headings[i].z *= -1.0
            elif self.balls[i].pos.x > (self.edges[2].pos.x - 6.5):
                self.headings[i].x *= -1.0
            elif self.balls[i].pos.x < (self.edges[3].pos.x + 6.5):
                self.headings[i].x *= -1.0

    def inPocket(self):
        '''checks to see if any of the game balls go 'into' a pocket
        and hides the ball unneath the surface'''
        returnValue = [0]
        listOfBalls = []
        whiteOut = False
        for i in range(16):
            A = ((50.0 + self.balls[i].pos.x)**2.0 + (25.0 + self.balls[i].pos.z)**2.0)**0.5
            B = ((50.0 - self.balls[i].pos.x)**2.0 + (25.0 - self.balls[i].pos.z)**2.0)**0.5
            C = ((50.0 - self.balls[i].pos.x)**2.0 + (25.0 + self.balls[i].pos.z)**2.0)**0.5
            D = ((50.0 + self.balls[i].pos.x)**2.0 + (25.0 - self.balls[i].pos.z)**2.0)**0.5
            E = ((self.balls[i].pos.x)**2.0 + (25.0 + self.balls[i].pos.z)**2.0)**0.5
            F = ((self.balls[i].pos.x)**2.0 + (25.0 - self.balls[i].pos.z)**2.0)**0.5
            
            if A < 6.0 or B < 6.0 or C < 6.0 or D < 6.0 or E < 4.24 or F < 4.24:
                if i == 15:
                    self.balls[i].pos.x = 55.0
                    self.balls[i].pos.y = 5.0
                    self.balls[i].pos.z = 0.0
                    self.headings[i].x = 0.0
                    self.headings[i].z = 0.0
                    self.balls[i].color = color.orange
                    whiteOut = True
                else:
                    self.balls[i].color = color.black
                    self.balls[i].pos.x = -55.0
                    self.balls[i].pos.y = -5.0
                    self.balls[i].pos.z = -30.0
                    self.headings[i].x = 0.0
                    self.headings[i].z = 0.0
                    self.balls[i].visible = False
                    if i in [0, 3, 5, 7, 10, 12, 14] and 2 not in returnValue:
                        returnValue += [2]
                    elif i == 4 and 3 not in returnValue:
                        returnValue += [3]
                    elif 4 not in returnValue:
                        returnValue += [4]
                    listOfBalls += [i]

        return [returnValue, listOfBalls, whiteOut]

    def setPosition(self, x, z):
        '''sets the position of the cue ball in relation to the user input'''
        xpos = self.balls[15].pos.x
        zpos = self.balls[15].pos.z
        if (x > 0.0 or xpos > 26.0) and (x < 0.0 or xpos < 36.5):
            self.cue.pos.x += x
            self.balls[15].x += x
        if (z > 0.0 or zpos > -23.0) and (z < 0.0 or zpos < 23.0):
            self.cue.pos.z += z
            self.balls[15].z += z

    def displayPower(self, factor):
        '''allows the user to assign the amount of power that will hit the cue ball'''
        self.cue.pos.x += self.headings[16].x * factor
        self.cue.pos.y += self.headings[16].y * factor
        self.cue.pos.z += self.headings[16].z * factor

    def reset(self, scratched):
        '''checks to see if the cue ball has gone inside of a pocket and then resets it back to the appropriate
        side of the table if a player does scratch'''
        if scratched:
            self.balls[15].color = color.white
            self.balls[15].pos.x = 31.25
            self.balls[15].pos.y = 1.5
            self.balls[15].pos.z = 0.0
        self.cue.visible = not self.cue.visible
        self.cue.pos = self.balls[15].pos + vector(1.5, 0.5, 0.0)
        self.headings[15] = vector(-1.0, 0.0, 0.0)
        self.headings[16] = vector(-0.8, -0.2, 0.0)
        self.cue.axis = (40, 10, 0)

    def clearBoard(self):
        '''clears the board of all balls so that it may be reset and another game may be played'''
        for i in range(16):
            self.balls[i].pos = vector(0, 0, 35)
            self.balls[i].visible = False
            self.cue.pos = vector(0, 0, 35)
            self.cue.axis = (0.1, 0, 0)
        self.cue.visible = False

    def blackOut(self, condition):
        '''causes a special 'blackout' mode where the players can only see the ball'''
        for i in range(4):
            self.legs[i].visible = not self.legs[i].visible
            self.edges[i].visible = not self.edges[i].visible
        self.surface.visible = not self.surface.visible
        for i in range(6):
            self.pockets[i].visible = not self.pockets[i].visible
        for i in range(18):
            self.dots[i].visible = not self.dots[i].visible

        if condition == "b":
            self.balls[4].color = (0.2, 0.2, 0.2)

    def checkPlacement(self):
        '''makes sure the user has placed the cue ball in a valid location'''
        for i in range(15):
            A = ((self.balls[i].pos.x - self.balls[15].pos.x)**2.0 + (self.balls[i].pos.z - self.balls[15].pos.z)**2.0)**0.5
            if A < 3.0:
                return False
        return True

    def scratchedBalls(self, whoseBall, listOfBalls):
        '''resets the position of balls hit in during a scratched shot'''
        resetBalls = []
        if whoseBall == 0 or len(listOfBalls) == 0:
            return
        elif whoseBall == 2:
            for i in range(len(listOfBalls)):
                if listOfBalls[i] in [0, 3, 5, 7, 10, 12, 14]:
                    resetBalls += [listOfBalls[i]]
        else:
            for i in range(len(listOfBalls)):
                if listOfBalls[i] in [1, 2, 6, 8, 9, 11, 13]:
                    resetBalls += [listOfBalls[i]]

        counter1 = 0
        counter2 = 0
        counter3 = 0
        for i in range(len(resetBalls)):
            j = 0
            if i in [1, 2]:
                j = 1
            elif i in [3, 4, 5]:
                j = 2
            else:
                j = 3
            self.balls[resetBalls[i]].visible = not self.balls[resetBalls[i]].visible
            if j == 0:
                self.balls[resetBalls[i]].pos = vector(-24.0, 1.5, 0.0)
            elif j == 1:
                self.balls[resetBalls[i]].pos = vector(-24.0 - 2.6 * j, 1.5, -1.5 * j + 3.0 * counter1)
                counter1 += 1
            elif j == 2:
                self.balls[resetBalls[i]].pos = vector(-24.0 - 2.6 * j, 1.5, -1.5 * j + 3.0 * counter2)
                counter2 += 1
            else:
                self.balls[resetBalls[i]].pos = vector(-24.0 - 2.6 * j, 1.5, -1.5 * j + 3.0 * counter3)
                counter3 += 1

        moveBack = True
        while moveBack:
            tempCondition = True
            for i in range(len(resetBalls)):
                for j in range(15):
                    if j != resetBalls[i]:
                        A = ((self.balls[resetBalls[i]].pos.x - self.balls[j].pos.x)**2.0 + (self.balls[resetBalls[i]].pos.z - self.balls[j].pos.z)**2.0)**0.5
                        if A < 3.0:
                            tempCondition = False
            if tempCondition:
                moveBack = False
            else:
                for i in range(len(resetBalls)):
                    self.balls[resetBalls[i]].pos += vector(-0.05, 0.0, 0.0)

        for i in range(len(resetBalls)):
            if whoseBall == 2:
                self.balls[resetBalls[i]].color = color.red
            elif whoseBall == 4:
                self.balls[resetBalls[i]].color = color.blue

    def simulateShot(self, power):
        '''simulates a shot by moving the cue stick from the the assigned distance(power) towards the cue ball.
        this doesn't actually hit the ball'''
        dt = 0.0002 * (power**2)
        A = ((self.cue.pos.x - self.balls[15].pos.x)**2.0 + (self.cue.pos.y - self.balls[15].pos.y)**2.0 + (self.cue.pos.z - self.balls[15].pos.z)**2.0)**0.5
        while A >= 1.0:
            self.cue.pos.x += self.headings[16].x * dt
            self.cue.pos.y += self.headings[16].y * dt
            self.cue.pos.z += self.headings[16].z * dt
            A = ((self.cue.pos.x - self.balls[15].pos.x)**2.0 + (self.cue.pos.y - self.balls[15].pos.y)**2.0 + (self.cue.pos.z - self.balls[15].pos.z)**2.0)**0.5
        self.cue.visible = not self.cue.visible
        self.cue.pos = vector(0.0, -2.5, 0.0)
        self.cue.axis = (-1, 0, 0)
            
    def strike(self, power, whoseBall):
        '''moves the cue ball towards the direction and with power chosen by the player'''
        velocity = 0.1 * power
        RATE = 1000
        condition = 0
        ball = whoseBall
        totalBallsOut = []
        whiteOut = False
        while velocity > 0.01:
            rate(RATE)
            for i in range(16):
                vx = self.headings[i].x * velocity
                vz = self.headings[i].z * velocity
                self.balls[i].pos.x += vx
                self.balls[i].pos.z += vz
            self.wallCollision()
            
            if ball == 0 and condition != 1:
                temp = self.inPocket()
                for i in range(len(temp[1])):
                    totalBallsOut += [temp[1][i]]
                if 3 in temp[0]:
                    condition = 1
                elif 2 in temp[0] and condition not in [1, 2, 3, 4]:
                    ball = 2
                    condition = 2
                elif 4 in temp[0] and condition not in [1, 2, 3, 4]:
                    ball = 4
                    condition = 4
                elif 5 in temp[0] and condition != 1:
                    condition = 3
                else:
                    condition = 0
                if whiteOut == False:
                    whiteOut = temp[2]
            
            elif ball == 0 and condition != 1:
                temp = self.inPocket()
                for i in range(len(temp[1])):
                    totalBallsOut += [temp[1][i]]
                if 3 in temp[0]:
                    condition = 1
                if whiteOut == False:
                    whiteOut = temp[2]
            
            elif ball == 2:
                temp = self.inPocket()
                for i in range(len(temp[1])):
                    totalBallsOut += [temp[1][i]]
                if 3 in temp[0]:
                    condition = 1
                elif 2 in temp[0] and condition != 1:
                    condition = 2
                if whiteOut == False:
                    whiteOut = temp[2]
            
            elif ball == 4:
                temp = self.inPocket()
                for i in range(len(temp[1])):
                    totalBallsOut += [temp[1][i]]
                if 3 in temp[0]:
                    condition = 1
                elif 4 in temp[0] and condition != 1:
                    condition = 4
                if whiteOut == False:
                    whiteOut = temp[2]
            
            collide = self.ballCollision(velocity)
            velocity *= 0.998
        for i in range(16):
            self.headings[i].x = 0.0
            self.headings[i].z = 0.0
        return [self.eightLeft(), condition, ball, totalBallsOut, whiteOut]

    def ballCollision(self, velocity):
        '''checks to see if any two balls collide and then makes them bounce in a realistic manner.'''
        f = []
        s = []
        for i in range(16):
            for j in range(i + 1, 16):
                A = ((self.balls[j].pos.x - self.balls[i].pos.x)**2.0 + (self.balls[j].pos.z - self.balls[i].pos.z)**2.0)**0.5
                if A < 3.0:
                    f += [i]
                    s += [j]
        if len(f) >= 1:
            for k in range(len(f)):
                A = ((self.balls[s[k]].pos.x - self.balls[f[k]].pos.x)**2.0 + (self.balls[s[k]].pos.z - self.balls[f[k]].pos.z)**2.0)**0.5
                if A == 0.0:
                    pass
                else:
                    ref1 = [(self.balls[f[k]].pos.x - self.balls[s[k]].pos.x)/A, (self.balls[f[k]].pos.z - self.balls[s[k]].pos.z)/A]
                    magr1 = (ref1[0]**2.0 + ref1[1]**2.0)**0.5
                    ref2 = [(self.balls[s[k]].pos.x - self.balls[f[k]].pos.x)/A, (self.balls[s[k]].pos.z - self.balls[f[k]].pos.z)/A]
                    magr2 = (ref2[0]**2.0 + ref2[1]**2.0)**0.5
                    magf = (self.headings[f[k]].x**2.0 + self.headings[f[k]].z**2.0)**0.5
                    mags = (self.headings[s[k]].x**2.0 + self.headings[s[k]].z**2.0)**0.5
                    plane1 = [-1.0 * ref1[1], ref1[0]]
                    mag1 = (plane1[0]**2.0 + plane1[1]**2.0)**0.5
                    plane2 = [ref1[1], -1.0 * ref1[0]]
                    mag2 = (plane2[0]**2.0 + plane2[1]**2.0)**0.5

                    cos1 = 0.0
                    cos2 = 0.0
                    if magf != 0.0:
                        cos1 = (self.headings[f[k]].x * plane1[0] + self.headings[f[k]].z * plane1[1]) / (magf * mag1)
                        cos2 = (self.headings[f[k]].x * plane2[0] + self.headings[f[k]].z * plane2[1]) / (magf * mag2)
                    partialf1 = [0.0, 0.0]
                    partials1 = [0.0, 0.0]
                    if magf == 0.0:
                        pass
                    elif cos1 < cos2:
                        factor = (self.headings[f[k]].x * plane1[0] + self.headings[f[k]].z * plane1[1]) / (mag1 * mag1)
                        partialf1 = [factor * plane1[0], factor * plane1[1]]
                    else:
                        factor = (self.headings[f[k]].x * plane2[0] + self.headings[f[k]].z * plane2[1]) / (mag2 * mag2)
                        partialf1 = [factor * plane2[0], factor * plane2[1]]

                    cos1 = 0.0
                    cos2 = 0.0
                    if mags != 0.0:
                        cos1 = (self.headings[s[k]].x * plane1[0] + self.headings[s[k]].z * plane1[1]) / (mags * mag1)
                        cos2 = (self.headings[s[k]].x * plane2[0] + self.headings[s[k]].z * plane2[1]) / (mags * mag2)
                    if mags == 0.0:
                        pass
                    elif cos1 < cos2:
                        factor = (self.headings[s[k]].x * plane1[0] + self.headings[s[k]].z * plane1[1]) / (mag1 * mag1)
                        partials1 = [factor * plane1[0], factor * plane1[1]]
                    else:
                        factor = (self.headings[s[k]].x * plane2[0] + self.headings[s[k]].z * plane2[1]) / (mag2 * mag2)
                        partials1 = [factor * plane2[0], factor * plane2[1]]

                    cos1 = 0.0
                    cos2 = 0.0
                    if magf != 0.0:
                        cos1 = (self.headings[f[k]].x * ref1[0] + self.headings[f[k]].z * ref1[1]) / (magf * magr1)
                        cos2 = (self.headings[f[k]].x * ref2[0] + self.headings[f[k]].z * ref2[1]) / (magf * magr2)
                    partialf2 = [0.0, 0.0]
                    partials2 = [0.0, 0.0]
                    if magf == 0.0:
                        pass
                    elif cos1 < cos2:
                        factor = (self.headings[f[k]].x * ref1[0] + self.headings[f[k]].z * ref1[1]) / (magr1 * magr1)
                        partials2 = [factor * ref1[0], factor * ref1[1]]
                    else:
                        factor = (self.headings[f[k]].x * ref2[0] + self.headings[f[k]].z * ref2[1]) / (magr2 * magr2)
                        partials2 = [factor * ref2[0], factor * ref2[1]]

                    cos1 = 0.0
                    cos2 = 0.0
                    if mags != 0.0:
                        cos1 = (self.headings[s[k]].x * ref1[0] + self.headings[s[k]].z * ref1[1]) / (mags * magr1)
                        cos2 = (self.headings[s[k]].x * ref2[0] + self.headings[s[k]].z * ref2[1]) / (mags * magr2)
                    if mags == 0.0:
                        pass
                    elif cos1 < cos2:
                        factor = (self.headings[s[k]].x * ref1[0] + self.headings[s[k]].z * ref1[1]) / (magr1 * magr1)
                        partialf2 = [factor * ref1[0], factor * ref1[1]]
                    else:
                        factor = (self.headings[s[k]].x * ref2[0] + self.headings[s[k]].z * ref2[1]) / (magr2 * magr2)
                        partialf2 = [factor * ref2[0], factor * ref2[1]]
                    
                    if (self.headings[f[k]].x < self.headings[s[k]].x and self.headings[f[k]].x < 0.0):
                        self.balls[f[k]].pos.x -= self.headings[f[k]].x * velocity
                        self.balls[f[k]].pos.z -= self.headings[f[k]].z * velocity
                    elif (self.headings[f[k]].x > self.headings[s[k]].x and self.headings[f[k]].x > 0.0):
                        self.balls[f[k]].pos.x -= self.headings[f[k]].x * velocity
                        self.balls[f[k]].pos.z -= self.headings[f[k]].z * velocity
                    elif (self.headings[f[k]].z < self.headings[s[k]].z and self.headings[f[k]].z < 0.0):
                        self.balls[f[k]].pos.x -= self.headings[f[k]].x * velocity
                        self.balls[f[k]].pos.z -= self.headings[f[k]].z * velocity
                    elif (self.headings[f[k]].z > self.headings[s[k]].z and self.headings[f[k]].z > 0.0):
                        self.balls[f[k]].pos.x -= self.headings[f[k]].x * velocity
                        self.balls[f[k]].pos.z -= self.headings[f[k]].z * velocity
                    else:
                        self.balls[s[k]].pos.x -= self.headings[s[k]].x * velocity
                        self.balls[s[k]].pos.z -= self.headings[s[k]].z * velocity
                    
                    self.headings[f[k]] = vector(partialf1[0] + partialf2[0], 0.0, partialf1[1] + partialf2[1])
                    self.headings[s[k]] = vector(partials1[0] + partials2[0], 0.0, partials1[1] + partials2[1])
            return True
        return False

    def turn(self, angle):
        '''allows the player to rotate the cue stick around the cue ball in the direction that they want'''
        theta = math.radians(angle)
        rotation_axis = vector(0, 1, 0)
        cOrigin = self.balls[15].pos
        self.cue.rotate(angle = theta, axis = rotation_axis, origin = cOrigin)
        self.headings[15] = rotate(self.headings[15], angle = theta, axis = rotation_axis)
        self.headings[16] = rotate(self.headings[16], angle = theta, axis = rotation_axis)

def main():
    '''runs the game with appropriate user input and calls functions in the board
    class to appropriately play the game of pool'''
    scene.autoscale = True
    scene.background = color.black
    scene.title = "Pool"
    board = Board()
    time.sleep(2)
    textColor = color.white
    instructions = label(pos = (0,0.25,0), color = textColor, text = " Welcome to our game of Pool!\n Turn instructions on/off with 'i'\n Move the cue ball with directional keys and set the cue ball with 's' \n Rotate the cue stick with 'c' and 'v' \n or rotate the cue stick faster with 'f' and 'g' and set with 's' \n Assign power with 'm' and 'l' and set with 's' ")
    time.sleep(15)
    whoseBall = 0
    condition = 0
    playerBalls = [0, 0]
    
    instructions.visible = not instructions.visible
    black = label(pos = (0, 15, 0), color = textColor, text = "Press 'b' if you would like to play in the Black Out mode\nPress 'w' if you would like to play in the White Out mode\nPress 's' to play a normal game")
    while True:
        if scene.kb.keys:
            s = scene.kb.getkey()
            if s == "b":
                board.blackOut("b")
                break
            if s == "w":
                board.blackOut("w")
                scene.background = color.white
                textColor = color.black
                break
            if s == "s":
                break
    black.visible = not black.visible
    
    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1: Please set the cue ball to the desired location.")
    time.sleep(2)
    tempScreen.visible = not tempScreen.visible
    
    while True:
        if scene.kb.keys:
            s = scene.kb.getkey()
            if s == "i":
                instructions.visible = not instructions.visible
            if s == "left":
                board.setPosition(0.0, 0.9)
            if s == "right":
                board.setPosition(0.0, -0.9)
            if s == "up":
                board.setPosition(-0.75, 0.0)
            if s == "down":
                board.setPosition(0.75, 0.0)
            if s == "s":
                break
    
    while playerBalls[0] == 0 and playerBalls[1] == 0:
        while condition == whoseBall:
            tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1's turn.")
            time.sleep(2)
            tempScreen.visible = not tempScreen.visible
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "c":
                        board.turn(-1.0)
                    if s == "f":
                        board.turn(-30.0)
                    if s == "v":
                        board.turn(1.0)
                    if s == "g":
                        board.turn(30.0)
                    if s == "s":
                        break
            power = 0
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "m" and power < 5:
                        board.displayPower(-3.0)
                        power += 1
                    if s == "l" and power > 0:
                        board.displayPower(3.0)
                        power -= 1
                    if s == "s":
                        break
            if power == 0:
                power = 1
                board.displayPower(-3.0)
            board.simulateShot(power)
            win = board.strike(power, whoseBall)
            if win[1] == 1:
                if instructions.visible:
                    instructions.visible = not instructions.visible
                if (playerBalls[0] == 2 and win[0] == 0) or (playerBalls[0] == 4 and win[0] == 2):
                    winScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 1 wins!")
                else:
                    lossScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 1 loses!")
                time.sleep(10)
                board.clearBoard()
                return
            if playerBalls[0] == 0:
                playerBalls[0] = win[2]
                whoseBall = playerBalls[0]
                if playerBalls[0] == 2:
                    playerBalls[1] = 4
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1 is red.\nPlayer 2 is blue.")
                    time.sleep(5)
                    tempScreen.visible = not tempScreen.visible
                elif playerBalls[0] == 4:
                    playerBalls[1] = 2
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1 is blue.\nPlayer 2 is red.")
                    time.sleep(5)
                    tempScreen.visible = not tempScreen.visible
            if win[4] == False:
                board.reset(False)
                if whoseBall != 0:
                    condition = win[1]
                else:
                    condition = 1
            else:
                board.reset(True)
                board.scratchedBalls(whoseBall, win[3])
                condition = 1
                placed = False
                while placed == False:
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 2: Please set the cue ball to the desired location.")
                    time.sleep(2)
                    tempScreen.visible = not tempScreen.visible
                    while True:
                        if scene.kb.keys:
                            s = scene.kb.getkey()
                            if s == "i":
                                instructions.visible = not instructions.visible
                            if s == "left":
                                board.setPosition(0.0, 0.9)
                            if s == "right":
                                board.setPosition(0.0, -0.9)
                            if s == "up":
                                board.setPosition(-0.75, 0.0)
                            if s == "down":
                                board.setPosition(0.75, 0.0)
                            if s == "s":
                                break
                    placed = board.checkPlacement()
        
        condition = playerBalls[1]
        whoseBall = playerBalls[1]
        
        while condition == whoseBall:
            tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 2's turn.")
            time.sleep(2)
            tempScreen.visible = not tempScreen.visible
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "c":
                        board.turn(-1.0)
                    if s == "f":
                        board.turn(-30.0)
                    if s == "v":
                        board.turn(1.0)
                    if s == "g":
                        board.turn(30.0)
                    if s == "s":
                        break
            power = 0
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "m" and power < 5:
                        board.displayPower(-3.0)
                        power += 1
                    if s == "l" and power > 0:
                        board.displayPower(3.0)
                        power -= 1
                    if s == "s":
                        break
            if power == 0:
                power = 1
                board.displayPower(-3.0)
            board.simulateShot(power)
            win = board.strike(power, whoseBall)
            if win[1] == 1:
                if instructions.visible:
                    instructions.visible = not instructions.visible
                if (playerBalls[1] == 2 and win[0] == 0) or (playerBalls[1] == 4 and win[0] == 2):
                    winScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 2 wins!")
                else:
                    lossScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 2 loses!")
                time.sleep(10)
                board.clearBoard()
                return
            if playerBalls[1] == 0:
                playerBalls[1] = win[2]
                whoseBall = playerBalls[1]
                if playerBalls[1] == 2:
                    playerBalls[0] = 4
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1 is blue.\nPlayer 2 is red.")
                    time.sleep(5)
                    tempScreen.visible = not tempScreen.visible
                elif playerBalls[1] == 4:
                    playerBalls[0] = 2
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1 is red.\nPlayer 2 is blue.")
                    time.sleep(5)
                    tempScreen.visible = not tempScreen.visible
            if win[4] == False:
                board.reset(False)
                if whoseBall != 0:
                    condition = win[1]
                else:
                    condition = 1
            else:
                board.reset(True)
                board.scratchedBalls(whoseBall, win[3])
                condition = 1
                placed = False
                while placed == False:
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1: Please set the cue ball to the desired location.")
                    time.sleep(2)
                    tempScreen.visible = not tempScreen.visible
                    while True:
                        if scene.kb.keys:
                            s = scene.kb.getkey()
                            if s == "i":
                                instructions.visible = not instructions.visible
                            if s == "left":
                                board.setPosition(0.0, 0.9)
                            if s == "right":
                                board.setPosition(0.0, -0.9)
                            if s == "up":
                                board.setPosition(-0.75, 0.0)
                            if s == "down":
                                board.setPosition(0.75, 0.0)
                            if s == "s":
                                break
                    placed = board.checkPlacement()

    while True:
        whoseBall = playerBalls[0]
        condition = playerBalls[0]
        
        while condition == whoseBall:
            tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1's turn.")
            time.sleep(2)
            tempScreen.visible = not tempScreen.visible
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "c":
                        board.turn(-1.0)
                    if s == "f":
                        board.turn(-30.0)
                    if s == "v":
                        board.turn(1.0)
                    if s == "g":
                        board.turn(30.0)
                    if s == "s":
                        break
            power = 0
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "m" and power < 5:
                        board.displayPower(-3.0)
                        power += 1
                    if s == "l" and power > 0:
                        board.displayPower(3.0)
                        power -= 1
                    if s == "s":
                        break
            if power == 0:
                power = 1
                board.displayPower(-3.0)
            board.simulateShot(power)
            win = board.strike(power, whoseBall)
            if win[1] == 1:
                if instructions.visible:
                    instructions.visible = not instructions.visible
                if (playerBalls[0] == 2 and win[0] == 0) or (playerBalls[0] == 4 and win[0] == 2):
                    winScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 1 wins!")
                else:
                    lossScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 1 loses!")
                time.sleep(10)
                board.clearBoard()
                return
            if win[4] == False:
                board.reset(False)
                condition = win[1]
            else:
                board.reset(True)
                board.scratchedBalls(whoseBall, win[3])
                condition = 1
                placed = False
                while placed == False:
                    tempScreen = label(pos = (0, 15, 0), text = "Player 2: Please set the cue ball to the desired location.")
                    time.sleep(2)
                    tempScreen.visible = not tempScreen.visible
                    while True:
                        if scene.kb.keys:
                            s = scene.kb.getkey()
                            if s == "i":
                                instructions.visible = not instructions.visible
                            if s == "left":
                                board.setPosition(0.0, 0.9)
                            if s == "right":
                                board.setPosition(0.0, -0.9)
                            if s == "up":
                                board.setPosition(-0.75, 0.0)
                            if s == "down":
                                board.setPosition(0.75, 0.0)
                            if s == "s":
                                break
                    placed = board.checkPlacement()
        
        condition = playerBalls[1]
        whoseBall = playerBalls[1]
        
        while condition == whoseBall:
            tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 2's turn.")
            time.sleep(2)
            tempScreen.visible = not tempScreen.visible
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "c":
                        board.turn(-1.0)
                    if s == "f":
                        board.turn(-30.0)
                    if s == "v":
                        board.turn(1.0)
                    if s == "g":
                        board.turn(30.0)
                    if s == "s":
                        break
            power = 0
            while True:
                if scene.kb.keys:
                    s = scene.kb.getkey()
                    if s == "i":
                        instructions.visible = not instructions.visible
                    if s == "m" and power < 5:
                        board.displayPower(-3.0)
                        power += 1
                    if s == "l" and power > 0:
                        board.displayPower(3.0)
                        power -= 1
                    if s == "s":
                        break
            if power == 0:
                power = 1
                board.displayPower(-3.0)
            board.simulateShot(power)
            win = board.strike(power, whoseBall)
            if win[1] == 1:
                if instructions.visible:
                    instructions.visible = not instructions.visible
                if (playerBalls[1] == 2 and win[0] == 0) or (playerBalls[1] == 4 and win[0] == 2):
                    winScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 2 wins!")
                else:
                    lossScreen = label(pos = (0, 0.25, 0), color = textColor, text = "Player 2 loses!")
                time.sleep(10)
                board.clearBoard()
                return
            if win[4] == False:
                board.reset(False)
                condition = win[1]
            else:
                board.reset(True)
                board.scratchedBalls(whoseBall, win[3])
                condition = 1
                placed = False
                while placed == False:
                    tempScreen = label(pos = (0, 15, 0), color = textColor, text = "Player 1: Please set the cue ball to the desired location.")
                    time.sleep(2)
                    tempScreen.visible = not tempScreen.visible
                    while True:
                        if scene.kb.keys:
                            s = scene.kb.getkey()
                            if s == "i":
                                instructions.visible = not instructions.visible
                            if s == "left":
                                board.setPosition(0.0, 0.9)
                            if s == "right":
                                board.setPosition(0.0, -0.9)
                            if s == "up":
                                board.setPosition(-0.75, 0.0)
                            if s == "down":
                                board.setPosition(0.75, 0.0)
                            if s == "s":
                                break
                    placed = board.checkPlacement()

if __name__ == "__main__":
    main()
