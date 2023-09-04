import random
import numpy as np
import matplotlib.pyplot as plt
class Person :
    def __init__(self):
        self.x = np . random . rand(2)*99
        self.v = np . random . rand(2)*10+5
        self . a = np . zeros (2)
        self . alive = True
        self . infected = False
        self . immune = False
        self . health = np . random . randint (50 ,150)
        self . bottom = np . random . randint ( -50 ,100)
    def __str__ ( self ) :
        st = ' '
        temps = vars ( self )
        for item in temps :
            st += str ( item ) + ': ' + str ( temps [ item ]) + '\n'
        return st
    
    def Move ( self , dt = 0.1) :
        self . x = self . x + self . v * dt + 0.5* self . a * dt * dt

    def Boundaries ( self ,V , H ) :
        if self . x [0] <0:
            self . x [0] *= -1
            self . v [0] *= -1
        if self . x [0] > H :
            self . x [0] = H - ( self . x [0] - H )
            self . v [0] *= -1
            # x [1] ve V[1] icin de
        if self . x [1] <0:
            self . x [1] *= -1
            self . v [1] *= -1
        if self . x [1] > H :
            self . x [1] = H - ( self . x [1] - H )
            self . v [1] *= -1
            
    def LowerHealth ( self ) :
        if self . infected == True and self . health > self . bottom:
            self . health -= 1

            
    def Cured ( self ) :
        if self . health <= self . bottom :
            self . infected = False
            self . immune = True

    def Death ( self ) :
        if self . health < 0:
            self . alive = False


    def Distance ( self , you ) :
        dist = np . sqrt ((( self .x - you . x ) **2) . sum () )
        return dist

    def Collide ( self , you ) :
        ypart = you . x [1] - self . x [1]
        xpart = you . x [0] - self . x [0]
        alpha = np . arctan2 ( ypart , xpart )
        R = np . array ((( np . cos ( - alpha ) ,- np . sin ( - alpha ) ) ,
                         ( np . sin ( - alpha ) , np . cos ( - alpha ) ) ) )
        vrot = R . dot ( self . v )
        wrot = vrot * np . array ((1 , -1) )
        R = np . array ((( np . cos ( alpha ) ,- np . sin ( alpha ) ) ,
                         ( np . sin ( alpha ) , np . cos ( alpha ) ) ) )
        w = R . dot ( wrot )
        self . v = w +0
        # enfeksiyon aktarımı
        if you . infected == True and self . immune == False :
            self . infected = True

            
def Iterate ( people , V , H ) :
    for me in people :
        if me . alive :
            me . Move ()
            me . Boundaries (V , H )
            me . LowerHealth ()
            me . Cured ()
            me . Death ()
            for you in people :
                if you . alive == True and me != you :
                    if me . Distance ( you ) < 1:
                        me . Collide ( you )
                        you . Collide ( me )

def CreateWorld ( NPeople,V,H) :
    people = []
    for i in range ( NPeople ) :
        people . append ( Person () )
    #print(people[NPeople-1])
    return people
#Bob=Person()
#print(Bob)


import matplotlib.pyplot as plt
people =CreateWorld (450,100,100)
for i in range ( 10 ) :
    people [ i ]. infected = True
    alives = []
    infects = []
for i in range ( 200 ) :
    Iterate ( people , 100 , 100 )
    ct = 0; cu =0
    for me in people :
        if me . alive :
            ct += 1
            if me . infected :
                cu += 1
    alives . append ( ct )
    infects . append ( cu )
plt . plot ( alives )
plt . plot ( infects )
plt . show ()
