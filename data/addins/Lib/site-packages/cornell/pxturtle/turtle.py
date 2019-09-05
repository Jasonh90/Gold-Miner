"""
The PyX drawing turtle

PyX uses the canvas abstraction, so must drawing happens in the Window.  However, this
class allows us to replace the TKinter Turtle and use its commands to draw to a document.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


class Turtle(object):
    """
    An instance represents a graphics turtle.
    
    A graphics turtle is a pen that is controlled by direction and movement. The turtle 
    is a cursor that that you control by moving it left, right, forward, or backward.  
    As it moves, it draws a line of the same color as  the Turtle. 
    
    Because this is the PyX version, the Turtle is not visible -- only the final results.
    
    :ivar heading: The heading of this turtle in degrees.
    :vartype heading: ``float``
    
    :ivar speed: The animation speed of this turtle.
    :vartype speed: ``int`` in 0..10
    
    :ivar color: The color of this turtle
    
    :ivar visible: Whether the turtle's icon is visible
    :vartype visible: ``bool``
    
    :ivar drawmode: Whether the turtle is in draw mode.
    :vartype drawmode: ``bool``
    
    :ivar x: The x-coordinate of this turtle
    :vartype x: ``float``
    
    :ivar y: The t-coordinate of this turtle
    :vartype y: ``float``
    """
    #PRIVATE ATTRIBUTES:
    #    _window: The window attached to this turtle
    #    _pather: The current path information for this turtle
    
    
    # MUTABLE PROPERTIES
    @property
    def heading(self):
        """
        The heading of this turtle in degrees.
        
        Heading is measured counter clockwise from due east.
        
        **invariant**: Value must be a ``float``
        """
        return self._heading
    
    @heading.setter
    def heading(self,value):
        assert type(value) in [int, float], "%s is not a valid number" % repr(value)
        self._heading = value
    
    @property
    def color(self):
        """color of this turtle.
        
        All subsequent draw commands (forward/back) draw using this color.
        If the color changes, it only affects future draw commands, not
        past ones.
        
        **Invariant**: Value must be either a string with a color name, a
        3 element tuple of floats between 0 and 1 (inclusive), or an object
        in an additive color model (e.g. RGB or HSV)."""
        return self._color
    
    @color.setter
    def color(self,value):
        from .window import is_valid_color, to_valid_color
        assert (is_valid_color(value)), "%s is not a valid color input" % repr(value)
        tmp = to_valid_color(value)
        if (self._color != tmp and self._dirty):
            self.flush()
        self._color = tmp
    
    @property
    def drawmode(self):
        """
        Whether the turtle is in draw mode.
        
        All drawing calls are active if an only if this mode is True
        
        **invariant**: Value must be a ``bool``
        """
        return self._isdown
    
    @drawmode.setter
    def drawmode(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        if self._isdown and not value and self._dirty:
            self.flush()
        self._isdown = value
    
    @property
    def origin(self):
        """
        The pen origin in the draw window.
        
        This property is used by the Window to reset the turtle. This is a "friend" property 
        and the invariant is not enforced.
        
        **invariant**: Value is pair of numbers
        """
        return self._origin
    
    @origin.setter
    def origin(self,value):
        self._origin = value
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._x
    
    @property
    def y(self):
        """
        The y-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._y
    
    @property
    def radangle(self):
        """
        The turtle heading in radians
        
        *This attribute may not be (directly) altered*
        """
        import math
        return self._heading*math.pi/180.0
    
    # DISABLED PROPERTIES
    # These properties only make sense in a visible window, but are recorded
    # for grading purposes.
    @property
    def speed(self):
        """
        The animation speed of this turtle.
        
        The speed is an integer from 0 to 10. Speed = 0 means that no animation takes 
        place. The methods forward/back makes turtle jump and likewise left/right make 
        the turtle turn instantly.
        
        Speeds from 1 to 10 enforce increasingly faster animation of line drawing and 
        turtle turning. 1 is the slowest speed while 10 is the fastest (non-instantaneous) 
        speed.
        
        **invariant**: Value must be an ``int`` in the range 0..10.
        """
        return self._speed
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0 or value <= 10), "%s is outside the range 0..10" % repr(value)
        self._speed = value
    
    @property
    def visible(self):
        """
        Whether the turtle's icon is visible.
        
        Drawing commands will still work while the turtle icon is hidden. There will just 
        be no indication of the turtle's current location on the screen.
        
        **Invariant**: Value must be a ``bool``
        """
        return self._visible
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._visible = value
    
    
    # BUILT-IN METHODS
    def __init__(self,screen,position=(0, 0), color='red', heading=180, speed=0):
        """
        Creates a new turtle to draw on the given screen.
        
        :param screen: window object that turtle will draw on.
        :type screen:  :class:`Window`
        
        :param position: initial turtle position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param color: initial turtle color (default red)
        :type color: see ``color``
        
        :param heading: initial turtle directions (default 180)
        :type heading:  ``int`` or ``float``
        
        :param speed: initial turtle speed (default 0)
        :type speed:  ``int`` 0..10
        """
        from .window import Window, is_valid_color, to_valid_color
        from pyx import path
        assert type(screen) == Window, "$s is not a Window object" % repr(screen)
        assert (is_valid_color(color)), "%s is not a valid color input" % repr(color)
        
        self._window = screen
        screen._addTurtle(self)
        self._heading = heading
        self._isdown = True
        self._speed  = speed
        self._visible = True
        self._dirty  = False
        
        self._color = to_valid_color(color)
        
        self._x = position[0]
        self._y = position[1]
        self._pather = path.path(path.moveto(self.x,self.y))
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this turtle. 
        :rtype:  ``bool``
        """
        return str(self.__class__)+str(self)
    
    # A printable representation of the turtle, giving its position, color, and heading
    def __str__(self):
        """
        :return: A readable string representation of this tuple. 
        :rtype:  ``bool``
        """
        return 'Turtle[position={}, color={}, heading={}]'.format((self.x,self.y), self.color, self.heading)
    
    def __del__(self):
        """
        Deletes this turtle object, removing it from the window.
        """
        self.clear()
        self._window._removeTurtle(self)
    
    
    # PUBLIC METHODS
    def forward(self,distance):
        """
        Moves the turtle forward by the given amount.
        
        This method draws a line if drawmode is True.
        
        :param distance: distance to move in pixels
        :type distance:  ``int`` or ``float``
        """
        import math
        from pyx import path
        assert (type(distance) in [int, float]), "%s is not a valid number" % repr(distance)
        
        # Compute where we are going to
        dx = math.cos(self.radangle)*distance
        dy = math.sin(self.radangle)*distance
        
        self._x += dx
        self._y += dy
        
        if (self._isdown):
            self._pather.append(path.lineto(self.x,self.y))
        else:
            self._pather.append(path.moveto(self.x,self.y))
        self._dirty = True
    
    def backward(self,distance):
        """
        Moves the turtle backward by the given amount.
        
        This method draws a line if drawmode is True.
        
        :param distance: distance to move in pixels
        :type distance:  ``int`` or ``float``
        """
        assert (type(distance) in [int, float]), "%s is not a valid number" % repr(distance)
        self.forward(-distance)
    
    def right(self,degrees):
        """
        Turns the turtle to the right by the given amount.
        
        Nothing is drawn when this method is called.
        
        :param degrees: amount to turn right in degrees
        :type degrees:  ``int`` or ``float``
        """
        assert (type(degrees) in [int, float]), "%s is not a valid number" % repr(degrees)
        self._heading -= degrees
        self._dirty = True
    
    def left(self,degrees):
        """
        Turns the turtle to the left by the given amount.
        
        Nothing is drawn when this method is called.
        
        :param degrees: amount to turn left in degrees
        :type degrees:  ``int`` or ``float``
        """
        assert (type(degrees) in [int, float]), "%s is not a valid number" % repr(degrees)
        self._heading += degrees
        self._dirty = True
    
    def move(self,x,y):
        """
        Moves the turtle to given position without drawing.
        
        This method does not draw, regardless of the drawmode.
        
        :param x: new x position for turtle
        :type x:  ``int`` or ``float``
        
        :param y: new y position for turtle
        :type y:  ``int`` or ``float``
        """
        from pyx import path
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        self._x = x
        self._y = y
        self._pather.append(path.moveto(x,y))
        self._dirty = True
    
    def clear(self):
        """
        Deletes the turtle's drawings from the window.
        
        This method does not move the turtle or alter its attributes.
        """
        from pyx import path
        self._window.clear()
        self._window._addTurtle(self)
        self._pather = path.path(path.moveto(self.x,self.y))
        self._dirty = False
    
    def reset(self):
        """
        Deletes the turtle's drawings from the window.
        
        This method re-centers the turtle and resets all attributes to their defaults.
        """
        self._x = self.origin[0]
        self._y = self.origin[1]
        self.clear()
        
        self.heading = 180
        self.color = 'red'
        self.speed = 0
    
    def flush(self):
        """
        Writes the current turtle path and color to the window.
        
        PyX drawing only supports one color per path.  Therefore, this must be called
        every time the turtle changes color.
        """
        from pyx import path        
        self._window.stroke(self._pather,self.color)
        self._pather = path.path(path.moveto(self.x,self.y))
        self._dirty = False


