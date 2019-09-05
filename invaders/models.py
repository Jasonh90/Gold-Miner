"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Jason Huang
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
     
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializer: Creates a new ship
        
        This initializer assigns dimensions using the constants imported from consts.py
        
        """
        self._movement = SHIP_MOVEMENT
        super().__init__(x=GAME_WIDTH/2,width = SHIP_WIDTH, height = SHIP_HEIGHT,
                          bottom = SHIP_BOTTOM, source = SHIP_IMAGE)


    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShip(self,input):
        """
        Moves ship given a distance to move 
        
        The height is not given explicitly, so you must compute it from the width and
        pixel list length.
        
        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        x = SHIP_MOVEMENT
        if input.is_key_down('left'):
            if(self.x - SHIP_WIDTH/2 - x > 0):
                self.x -= x
        if input.is_key_down('right'):
            if(self.x + SHIP_WIDTH/2 + x < GAME_WIDTH):
                self.x += x
        
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        upleft = (bolt.left,bolt.y + bolt.height/2)
        upright = (bolt.left,bolt.y - bolt.height/2)
        botleft = (bolt.right,bolt.y + bolt.height/2)
        botright = (bolt.right,bolt.y - bolt.height/2)
        
        if(bolt.name=='alien' and (self.contains(upleft) or self.contains(upright)\
                    or self.contains(botleft) or self.contains(botright))):
            return True
        else:
            return False
    

class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getSpeed(self):
        return self._speed
    def setSpeed(self,speed):
        self._speed = self._speed * speed
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,**keywords):
        """
        Initializes one alien
        
        Calls GImage to create alien using keywords
        """
        super().__init__(**keywords)
        self._speed = ALIEN_SPEED
        
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        upleft = (bolt.left,bolt.y + bolt.height/2)
        upright = (bolt.left,bolt.y - bolt.height/2)
        botleft = (bolt.right,bolt.y + bolt.height/2)
        botright = (bolt.right,bolt.y - bolt.height/2)
        
        if(bolt.name=='player' and (self.contains(upleft) or self.contains(upright)\
                    or self.contains(botleft) or self.contains(botright))):
            return True
        else:
            return False
        
        
    

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Return: velocity of bolt
        """
        return self._velocity
        
        
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,**keywords):
        """
        Initializes a Bolt
        
        
        """
        
        super().__init__(height = BOLT_HEIGHT, width = BOLT_WIDTH, fillcolor = 'red',
                         linecolor = 'red',**keywords)
        self._velocity = BOLT_SPEED
        
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Checks if the bolt is coming from the ship
        
        Return: True if the name of the bolt is 'player'
        """
        if(self.name == 'player'):
            return True
        return False
    
    
    def isAlienBolt(self):
        """
        Checks if the bolt is coming from the ship
        
        Return: True if the name of the bolt is 'player'
        """
        if(self.name == 'alien'):
            return True
        return False
    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE