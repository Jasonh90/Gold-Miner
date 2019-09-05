# tkturtle.py (PyX version)
# Walker M. White (wmw2)
# August 20, 2015
"""
The PyX version of the drawing pen

PyX uses the canvas abstraction, so must drawing happens in the Window.  However, this
class allows us to replace the TKinter Pen and use its commands to draw to a document.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


class Pen(object):
    """
    An instance represents a graphics pen.
    
    A graphics pen is like a turtle except that it does not have a heading, and there is 
    no drawmode ``attribute``. Instead, the pen relies on explicit drawing commands such
    as :meth:`drawLine` or :meth:`drawCircle`.
    
    Another difference with the pen is that it can draw solid shapes.  The pen has an 
    attribute called ``fill``.  When this attribute is set to True, it will fill the 
    insides of any polygon traced by its drawLine method. However, the fill will not be 
    completed until fill is set to False, or the move method is invoked.
    
    Because this is the PyX version, the Pen is not visible -- only the final results.
    
    :ivar speed: The animation speed of this pen.
    :vartype speed: ``int`` in 0..10
    
    :ivar fill: Whether the pen's is drawing a solid shape
    :vartype fill: ``bool``
    
    :ivar pencolor: The outlining color of this pen
    
    :ivar fillcolor: The solid color of this pen
    
    :ivar visible: Whether the pen's icon is visible
    :vartype visible: ``bool``
    
    :ivar origin: the pen origin in the draw window
    :vartype origin: 2D ``tuple``
    
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
    def fill(self):
        """
        The fill status of this pen.
        
        If the fill status is True, then the pen will fill the insides of any polygon or 
        circle subsequently traced by its :meth:`drawLine` and :meth:`drawCircle` method. 
        If the attribute changes, it only affects future draw commands, not past ones. 
        Switching this attribute between True and False allows the pen to draw both solid 
        and hollow shapes.
        
        **invariant**: Value must be an ``bool``.
        """
        return self._filled
    
    @fill.setter
    def fill(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        if (self._dirty):
            self.flush()
        self._filled = value
    
    @property
    def pencolor(self):
        """
        The pen color of this pen.
        
        The pen color is used for drawing lines and circles. All subsequent draw commands 
        draw using this color. If the color changes, it only affects future draw commands, 
        not past ones.
        
        This color is only used for lines and the border of circles.  It is not the color 
        used for filling in solid areas (if the ``fill`` attribute  is True).  See the 
        attribute ``fillcolor`` for solid shapes.
        
        **invariant**: Value must be either a string with a color name, a 3 element tuple 
        of floats between 0 and 1 (inclusive), or an object in an additive color model 
        (e.g. RGB or HSV).
        """
        return self._pencolor
    
    @pencolor.setter
    def pencolor(self,value):
        from .window import is_valid_color, to_valid_color
        assert (is_valid_color(value)), "%s is not a valid color input" % repr(value)
        tmp = to_valid_color(value)
        if (self._pencolor != tmp and self._dirty):
            self.flush()
        self._pencolor = tmp
    
    @property
    def fillcolor(self):
        """
        The fill color of this turtle.
        
        The fill color is used for filling in solid shapes. If the ``fill`` attribute is 
        True, all subsequent draw commands fill their insides using this color.  If the 
        color changes, it only affects future draw commands, not past ones.
        
        This color is only used for filling in the insides of solid shapes.  It is not 
        the color used for the shape border.  See the attribute ``pencolor`` for the 
        border color.
        
        **invariant**: Value must be either a string with a color name, a 3 element tuple 
        of floats between 0 and 1 (inclusive), or an object in an additive color model 
        (e.g. RGB or HSV).
        """
        return self._fillcolor
    
    @fillcolor.setter
    def fillcolor(self,value):
        from .window import is_valid_color, to_valid_color
        assert (is_valid_color(value)), "%s is not a valid color input" % repr(value)
        tmp = to_valid_color(value)
        if (self._fillcolor != tmp and self._dirty):
            self.flush()
        self._fillcolor = tmp
    
    @property
    def origin(self):
        """
        The pen origin in the draw window.
        
        This property is used by the Window to reset the pen. This is a "friend" property 
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
        The x-coordinate of this pen.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._x
    
    @property
    def y(self):
        """
        The y-coordinate of this pen.
        
        To change the y coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*
        """
        return self._y
    
    
    # DISABLED PROPERTIES
    # These properties only make sense in a visible window, but are recorded
    # for grading purposes.
    @property
    def speed(self):
        """
        The animation speed of this pen.
        
        The speed is an integer from 0 to 10. Speed = 0 means that no animation takes 
        place. The :meth:`drawLine` and :meth:`drawCircle` methods happen instantly with 
        no animation.
        
        Speeds from 1 to 10 enforce increasingly faster animation of line drawing. 1 is 
        the slowest speed while 10 is the fastest (non-instantaneous) speed.
        
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
        Whether the pen's icon is visible.
        
        Drawing commands will still work while the pen icon is hidden. There will just be 
        no indication of the pen's current location on the screen.
        
        **invariant**: Value must be a ``bool``
        """
        return self._visible
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._visible = value
    
    @property
    def color(self):
        """
        Silent, unsupported property requested by a beta tester
        """
        assert False, 'Pen does not have a color; use pencolor or fillcolor'
    
    @color.setter
    def color(self,value):
        assert False, 'Pen does not have a color; use pencolor or fillcolor'
    
    
    # BUILT-IN METHODS
    def __init__(self,screen,position=(0, 0), color='red', speed=0):
        """
        Creates a new pen to draw on the given screen.
        
        The color will be assigned to both the pencolor and the fillcolor.
        
        :param screen: window object that pen will draw on.
        :type screen:  :class:`Window`
        
        :param position: initial pen position (origin is screen center)
        :type position:  2D ``tuple``
        
        :param color: initial pen color (default red)
        :type color: see ``color``
        
        :param heading: initial pen directions (default 180)
        :type heading:  ``int`` or ``float``
        
        :param speed: initial pen speed (default 0)
        :type speed:  ``int`` 0..10
        """
        from .window import Window, is_valid_color, to_valid_color
        from pyx import path
        assert type(screen) == Window, "$s is not a Window object" % repr(screen)
        assert (is_valid_color(color)), "%s is not a valid color input" % repr(color)
        
        self._window = screen
        screen._addPen(self)
        self._isdown = True
        self._filled = False
        self._dirty  = False
        self._speed  = speed
        self._visible = True
        
        self._pencolor  = to_valid_color(color)
        self._fillcolor = self._pencolor
        
        self._x = position[0]
        self._y = position[1]
        self._pather = path.path(path.moveto(self.x,self.y))
    
    def __repr__(self):
        """
        :return: An unambiguous string representation of this turtle. 
        :rtype:  ``bool``
        """
        return str(self.__class__)+str(self)
        
    def __str__(self):
        """
        :return: A readable string representation of this tuple. 
        :rtype:  ``bool``
        """
        return 'Pen(position={}, pencolor={}, fillcolor={})'.format((self.x,self.y), self.pencolor, self.fillcolor)
    
    def __del__(self):
        """
        Deletes this pen object, removing it from the window.
        """
        self.clear()
        self._window._removePen(self)
    
    
    # PUBLIC METHODS
    def move(self,x,y):
        """
        Moves the pen to given position without drawing.
        
        If the ``fill`` attribute is currently True, this method will complete the fill 
        before moving to the new region. The space between the original position and (x,y) 
        will not be connected.
        
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
    
    def drawLine(self, dx, dy):
        """
        Draws a line segment (dx,dy) from the current pen position
        
        The line segment will run from (x,y) to (x+dx,y+dy), where (x,y) is the current 
        pen position.  When done, the pen will be at position (x+dx,y+dy)
        
        :param dx: change in the x position
        :type dx:  ``int`` or ``float``
        
        :param dy: change in the y position
        :type dy:  ``int`` or ``float``
        """
        from pyx import path
        assert (type(dx) in [int, float]), "%s is not a valid number" % repr(dx)
        assert (type(dy) in [int, float]), "%s is not a valid number" % repr(dy)
        self._x += dx
        self._y += dy
        self._pather.append(path.lineto(self._x,self._y))
        self._dirty = True
    
    def drawTo(self, x, y):
        """
        Draws a line from the current pen position to (x,y)
        
        When done, the pen will be at (x, y).
        
        :param x: finishing x position for line
        :type x:  ``int`` or ``float``
        
        :param y: finishing y position for line
        :type y:  ``int`` or ``float``
        """
        from pyx import path
        assert (type(x) in [int, float]), "%s is not a valid number" % repr(x)
        assert (type(y) in [int, float]), "%s is not a valid number" % repr(y)
        self._x = x
        self._y = y
        self._pather.append(path.lineto(x,y))
        self._dirty = True
    
    def drawCircle(self, r, steps=20):
        """
        Draws a circle of radius r centered on the pen.
        
        The center of the circle is the current pen coordinates. When done, the position 
        of the pen will remain unchanged
        
        :param r: radius of the circle
        :type r:  ``int`` or ``float``
        """
        from pyx import path
        import math
        assert (type(r) in [int, float]), "%s is not a valid number" % repr(r)
        for s in range(steps):
            a = (math.pi*2*s)/float(steps)
            x = math.cos(a)*r+self._x
            y = math.sin(a)*r+self._y
            if s == 0:
                self._pather.append(path.moveto(x,y))
            else:
                self._pather.append(path.lineto(x,y))
        x = r+self._x
        y = self._y
        self._pather.append(path.lineto(x,y))
        self._dirty = True
    
    
    # PUBLIC METHODS
    def clear(self):
        """
        Deletes the pen's drawings from the window.
        
        This method does not move the pen or alter its attributes.
        """
        from pyx import path
        self._window.clear()
        self._window._addPen(self)
        self._pather = path.path(path.moveto(self.x,self.y))
        self._dirty = False
    
    def reset(self):
        """
        Deletes the pen's drawings from the window.
        
        This method re-centers the pen and resets all attributes to their defaults.
        """
        from .window import to_valid_color
        self._x = self.origin[0]
        self._y = self.origin[1]
        self.clear()
        
        self._pencolor  = to_valid_color('red')
        self._fillcolor = self._pencolor
        self.speed = 0
    
    def flush(self):
        """
        Writes the current turtle path and color to the window.
        
        PyX drawing only supports one color per path.  Therefore, this must be called 
        every time the turtle changes color.
        """
        from pyx import path
        if (self.fill):
            self._window.fill(self._pather,self.fillcolor)
        else:
            self._window.stroke(self._pather,self.pencolor)
        
        self._pather = path.path(path.moveto(self.x,self.y))
        self._dirty = False


