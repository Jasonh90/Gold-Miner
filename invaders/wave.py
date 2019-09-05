"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Jason Huang
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _alienDirection: the direction the aliens are heading (used in update only)
            [either 'right' or 'left']
        _fireRate: the speed at which the aliens fire a bolt
            [random int between 1 and BOLT_RATE]
        _alienMove: the amount of times the aliens have moved since the last bolt
            [int >= 0]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Return: ship
        """
        return self._ship
    
    def aliensRemaining(self):
        """
        Return: the amount of aliens remaining
        """
        remains = 0
        for row in self._aliens:
            for alien in row:
                if(alien!=None):
                    remains += 1
        return remains
    
    def getLives(self):
        """
        Returns: The amount of lives left for the player remaining
        """
        return self._lives
    
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a wave
        """
        self._ship = Ship()
        self._aliens = self._alienlist()
        self._bolt = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE]\
                                ,linewidth=2,linecolor='black')
        self._lives = SHIP_LIVES
        self._time = 0
        self._alienDirection = 'right'
        self._fireRate = random.randint(1,BOLT_RATE)
        self._alienMove = 0
        
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Updates the screen to move the ship left and right
        
        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        
        Parameter dt: keeps track of time in seconds
        Precondition: int > 0
        """
        if(self._ship == None):
            self._ship = Ship()
        self._ship.moveShip(input)
        self._time += dt
        self._moveAlien()
        if(self._bolt == [] or (self._isAlienBoltPresent() and len(self._bolt)<2)):
            self._checkFireKey(input)
        for bolt in self._bolt:
            if(not bolt.isPlayerBolt() and not bolt.isAlienBolt()):
                self._checkFireKey(input)
            elif(bolt.isPlayerBolt() and self._checkCeiling(bolt)):
                self._bolt.remove(bolt)
            if(bolt.isAlienBolt() and self._checkFloor(bolt)):
                self._bolt.remove(bolt)
            if(bolt.name == 'alien' and self._ship.collides(bolt)):
                self._bolt=[]
                self._ship = None
                for y in range(ALIEN_ROWS-1,-1,-1):
                    for x in range(ALIENS_IN_ROW-1,-1,-1):
                        if(self._aliens[y][x]!=None):
                            self._aliens[y][x].x=(x+1)*(ALIEN_H_SEP+ALIEN_WIDTH/2)+x*ALIEN_WIDTH/2
                            self._aliens[y][x].y=GAME_HEIGHT-ALIEN_CEILING-ALIEN_HEIGHT/2-y*(ALIEN_HEIGHT+ALIEN_V_SEP)
                self._lives -= 1
            self._alienCollides(bolt)
                
        if((self._alienMove == self._fireRate or self._fireRate==0) and\
            not self._isAlienBoltPresent()):
            self._alienShoot()
            self._fireRate = random.randint(0,BOLT_RATE)
            self._alienMove = 0
        # 18
        
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws each alien in the list of aliens
        
        Parameter view: the game view, used in drawing (see examples from class)
        Precondition: instance of GView; it is inherited from GameApp
        """
        for row in self._aliens:
            for alien in row:
                if(alien!=None):
                    alien.draw(view)
        self._dline.draw(view)
        if(self._ship!=None):
            self._ship.draw(view)
        for bolt in self._bolt:
            bolt.draw(view)
        
        
    # HELPER METHODS FOR UPDATE
    def _alienCollides(self,bolt):
        """
        Removes the alien that got hit by the bolt (makes the spot None)
        
        Parameter bolt: the bolt to check if it hit any aliens
        Precondition: Bolt class 
        """
        # only checks if the bolt is a player bolt and not an alien bolt
        if(bolt.name=='player'):
            for row in range(ALIEN_ROWS):
                for col in range(ALIENS_IN_ROW):
                    if(self._aliens[row][col]!=None):
                        if(self._aliens[row][col].collides(bolt)):
                            self._aliens[row][col] = None
                            self._bolt.remove(bolt)
                            self._alienSpeedUp()
                            
        
    def _alienSpeedUp(self):
        for row in self._aliens:
            for alien in row:
                if(alien!=None):
                    alien.setSpeed(0.97)
    def _moveAlien(self):
        """
        Moves all the aliens with a helper function
        """
        alienSpeed=self._alienAlive('right').getSpeed()
        RisAtBorder = self._alienAlive('right').right + ALIEN_H_WALK > GAME_WIDTH
        LisAtBorder = self._alienAlive('left').left - ALIEN_H_WALK < 0
        if(self._time>alienSpeed and not RisAtBorder and self._alienDirection=='right'):
            self._moveAlienHelper(ALIEN_H_WALK,'right')
        elif(self._time>alienSpeed and not LisAtBorder and self._alienDirection == 'left'):
            self._moveAlienHelper(ALIEN_H_WALK,'left')
        elif(self._time>alienSpeed and (LisAtBorder or RisAtBorder)):
            self._moveAlienHelper(ALIEN_V_WALK,'down')
            if LisAtBorder:
                self._alienDirection = 'right'
            if RisAtBorder:
                self._alienDirection = 'left'
                
    def _alienAlive(self,direction):
        """
        helps with _moveAlien to check which side aliens are alive
        if side aliens are dead, check the insides
        
        Parameter direction: The side to check
        Precondition: str (either 'right' or 'left')
        """
        if(direction == 'right'):
            for col in range(ALIENS_IN_ROW-1,-1,-1):
                for row in range(ALIEN_ROWS):
                    if(self._aliens[row][col]!=None):
                        return self._aliens[row][col]
        if(direction == 'left'):
            for col in range(ALIENS_IN_ROW):
                for row in range(ALIEN_ROWS):
                    if(self._aliens[row][col]!=None):
                        return self._aliens[row][col]
        
        
    def _moveAlienHelper(self,x,direction):
        """
        Moves the aliens right, left, or down, depending on where they are
        
        Parameter x: the amount each alien should move
        Precondition: int >= 0
        
        Parameter direction: the Direction the aliens are heading
        Precondition: str (either 'right','left','down')
        """
        if direction == 'right':
            for row in self._aliens:
                for alien in row:
                    if(alien!=None):
                        alien.x += x
        if direction == 'left':
            for row in self._aliens:
                for alien in row:
                    if(alien!=None):
                        alien.x -= x
        if direction == 'down':
            for row in self._aliens:
                for alien in row:
                    if(alien!=None):
                        alien.y -= x
        self._time = 0
        if(not self._isAlienBoltPresent()):
            self._alienMove += 1
            
            
    def _isAlienBoltPresent(self):
        """
        Checks if there's an alien bolt present on screen
        """
        for bolt in self._bolt:
            if bolt.name == 'alien':
                return True
        return False
    

    # HELPER METHODS 
    def _checkFireKey(self,input):
        """
        Checks if the player clicks 'space' or 'up'
        
        If player clicks either of those, this method will return add a player bolt
        into the list self._bolt
        
        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        curr_key = input.is_key_down('spacebar') or input.is_key_down('up')
        
        if(curr_key == True):
            self._bolt.append(Bolt(x = self._ship.x ,\
                                   y = self._ship.y + self._ship.height/2,\
                                   name = 'player'))
        
    
    def _checkCeiling(self, bolt):
        """
        Returns True if player's bolt passes the ceiling
        
        Parameter bolt_index: index at which the player's bolt as at in self._bolt
        Precondition: bolt_index is an int >= 0
        """
        if(bolt.y - bolt.height/2 > GAME_HEIGHT):
            return True
        else:
            bolt.y += bolt.getVelocity()
            return False
        
        
    def _checkFloor(self, bolt):
        """
        Returns True if alien's bolt passes the floor
        
        Parameter bolt_index: index at which the alien's bolt as at in self._bolt
        Precondition: bolt_index is an int >= 0
        """
        if(bolt.y + bolt.height/2 < 0):
            return True
        else:
            bolt.y -= bolt.getVelocity()
            return False


    def _alienShoot(self):
        """
        Procedure for an alien to create a bolt (put into self._bolt)
        """
        alien_str = self._pickAlien()
        row = int(alien_str[:alien_str.index(',')])
        col = int(alien_str[alien_str.index(',')+1:])
        alien = self._aliens[row][col]
        self._bolt.append(Bolt(x = alien.x,
                               y = alien.y - alien.height/2,
                               name = 'alien'))
        
    def _pickAlien(self):
        """
        Return: random alien to fire bolt
        
        Chooses random column that has an alien inside
        picks the lowest row that has an alien in that random column
        """
        col = random.randint(0,ALIENS_IN_ROW-1)
        # chooses another col if the first col is empty
        while(self._isColEmpty(col)): 
            col = random.randint(0,ALIENS_IN_ROW-1)
        for row in range(ALIEN_ROWS-1,-1,-1):
            if(self._aliens[row][col]!=None):
                return str(row)+','+str(col)
        
        
    def _isColEmpty(self,col):
        """
        Return: True if there's no alien in the whole column, False otherwise
        """
        for row in range(ALIEN_ROWS):
            if(self._aliens[row][col]!=None):
                return False
        return True
    
    
    # helper function for __init__
    def _alienlist(self):
        """
        Returns: a rectangular 2d list of aliens
        """
        list = []
        partlist = []
        count = 0 # keeps track of which image to use
        for y in range(ALIEN_ROWS-1,-1,-1):
            for x in range(ALIENS_IN_ROW-1,-1,-1):
                partlist.insert(0,Alien(x=(x+1)*(ALIEN_H_SEP+ALIEN_WIDTH/2)+x*ALIEN_WIDTH/2,
                    y=GAME_HEIGHT-ALIEN_CEILING-ALIEN_HEIGHT/2-y*(ALIEN_HEIGHT+ALIEN_V_SEP),
                                         height=ALIEN_HEIGHT,
                                         width=ALIEN_WIDTH,
                                         source=ALIEN_IMAGES[count//2%len(ALIEN_IMAGES)]))
            # increments count after every row filled
            count += 1
            list.insert(0,partlist)
            partlist = []
        return list
        