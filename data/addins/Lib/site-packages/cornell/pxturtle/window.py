"""
A PyX drawing window

This module abstracts the drawing window as an area within a LaTeX document.  This allows
us to produce a printed output of the student's work.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


class Window(object):
    """
    An instance is a portions of a graphics file.
    
    The window is a part of a page in a graphics file.  The exact placement on the page 
    is determined by the window dimensions AND the scaling factor.  By default, a window 
    has the same dimensions as a Tcl/TK window, but this requires a non-trivial scaling 
    factor in order to fit it on a page.
    
    Window objects are designed to write to PyX canvas object.  See the method 
    :meth:`flush`..
    
    :ivar x: The x coordinate for bottom left corner, measured in points
    :vartype x: ``int`` >= 0
    
    :ivar y: The y coordinate for bottom left corner, measured in points
    :vartype y: ``int`` >= 0
    
    :ivar width: The width of the window in points
    :vartype width: ``int`` > 0
    
    :ivar height: The height of the window in points
    :vartype height: ``int`` > 0
    
    :ivar title: The title displayed at top of window bar
    :vartype title: ``str``
    
    :ivar scale: The amount to scale the window, when put to page
    :vartype scale: ``float`` > 0
    
    :ivar mark: Whether Window has been used since last marking
    :vartype mark: ``bool``
    
    :ivar turtles: The tuple of all turtles attached to this Window
    :vartype turtles: ``tuple``
    
    :ivar pens: The tuple of all pens attached to this Window
    :vartype pens: ``tuple``
    """
    #PRIVATE ATTRIBUTES:
    #    _canvas: The backing store for this window
    
    
    # MUTABLE PROPERTIES
    @property
    def title(self):
        """
        The title displayed at top of window bar
        
        **invariant**: title must be a ``str``
        """
        return self._title
    
    @title.setter
    def title(self,value):
        assert (type(value) == str), "%s is not a string" % repr(value)
        self._title = value
    
    @property
    def x(self):
        """
        The x coordinate for lower left corner, measured in points
        
        **invariant**: x must be an ``int`` > 0
        """
        return self._x
    
    @x.setter
    def x(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._x = value
    
    @property
    def y(self):
        """
        The y coordinate for lower left corner, measured in points
        
        **invariant**: y must be an ``int`` > 0
        """
        return self._y
    
    @y.setter
    def y(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value >= 0), "%s is negative" % repr(value)
        self._y = value
    
    @property
    def width(self):
        """
        The width of the window in points
        
        **Invariant**: width must be an ``int`` > 0
        """
        return self._width
    
    @width.setter
    def width(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._width = value
    
    @property
    def height(self):
        """
        The height of the window in points
        
        **Invariant**: height must be an ``int`` > 0
        """
        return self._height
    
    @height.setter
    def height(self,value):
        assert (type(value) == int), "%s is not an int" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._height = value
    
    @property
    def scale(self):
        """
        The amount to scale the window, when put to page
        
        When the window is drawn, the points of the drawn image are
        multiplied by the scale factor.
        
        **invariant**: scale must be a ``float`` > 0
        """
        return self._scale
    
    @scale.setter
    def scale(self,value):
        assert (type(value) in [int, float]), "%s is not a number" % repr(value)
        assert (value > 0), "%s is not positive" % repr(value)
        self._scale = value
    
    @property
    def mark(self):
        """
        Whether Window has been used since last marking
        
        **invariant**: Value is a ``bool``
        """
        return self._mark
    
    @mark.setter
    def mark(self,value):
        assert (type(value) == bool), "%s is not a bool" % repr(value)
        self._mark = value
    
    # IMMUTABLE PROPERTIES
    @property
    def turtles(self):
        """
        The tuple of all turtles attached to this Window
        
        *This attribute may not be altered directly*
        """
        return self._turtles[:]
    
    @property
    def pens(self):
        """
        The tuple of all pens attached to this Window
        
        *This attribute may not be altered directly*
        """
        return self._pencils[:]
    
    # FRIEND PROPERTIES
    @property
    def speed(self):
        """
        The speed of the last pen or turtle to draw to this window.
        """
        return self._lastspeed
    
    @property
    def visibility(self):
        """
        The visibility of the last pen or turtle to draw to this window
        """
        return self._lastviz
    
    # UNUSED PROPERTIES
    @property
    def resizable(self):
        """
        Whether or not the Window supports user resizing
        
        This is not supported in the PyX version
        
        **invariant**: resizable must be a ``bool``
        """
        raise NotImplementedError('resizable is not implemented in the PyX version')
    
    @property
    def refresh(self):
        """
        How often to refresh the screen when drawing the turtle
        
        This is not supported in the PyX version
        
        **invariant**: refresh must be an ``int`` >= 0
        """
        raise NotImplementedError('refresh is not implemented in the PyX version')
    
    
    # BUILT-IN METHODS
    def __init__(self,x=0,y=0,width=600,height=600, scale=1):
        """
        Creates a new Window to support turtle graphics
        
        :param x: initial x coordinate (default 100)
        :type x: ``int`` >= 0
        
        :param y: initial y coordinate (default 100)
        :type y: ``int`` >= 0
        
        :param width: initial window width (default 800)
        :type width: ``int`` > 0
        
        :param height: initial window height (default 800)
        :type height: ``int`` > 0
        
        :param scale: initial window scale (default 1)
        :type scale:  ``float`` > 0
        """
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        self.scale  = scale
        self._title = None
        self._mark  = False
        self._lastspeed = -1
        self._lastviz   = False
        self.clear()
    
    def __del__(self):
        """
        Destroys this window and its associated assets
        """
        self._turtles = []
        self._pencils = []
        del self._canvas
    
    
    # FRIEND METHODS
    def _addTurtle(self,turt):
        """
        Adds a turtle to this window.
        
        :param turt: the graphics turtle
        :type turt:  ``Turtle``
        """
        from .turtle import Turtle
        assert (type(turt) == Turtle), "%s is not a valid Turtle object" % repr(turt)
        assert turt not in self._turtles, "%s is already a member of thiw Window" % repr(turt)
        
        # Center the turtle.
        turt.origin = (self._width/2, self._height/2)
        self._turtles.append(turt)
        self._mark = True
    
    def _addPen(self,pen):
        """
        Adds a pen to this window.
        
        :param pen: the graphics pen
        :type pen:  ``Pen``
        """
        from .pen import Pen
        assert (type(pen) == Pen), "%s is not a valid graphics pen" % repr(pen)
        assert pen not in self._pencils, "%s is already a member of thiw Window" % repr(pen)
        pen.origin = (self._width/2, self._height/2)
        
        # Center the pen.
        self._pencils.append(pen)
        self._mark = True
    
    def _removeTurtle(self,turt):
        """
        Removes a turtle from this window.
        
        :param turt: the graphics turtle
        :type turt:  ``Turtle``
        """
        if turt in self._turtles:
            self._turtles.remove(turt)
        self._mark = True
    
    def _removePen(self,pen):
        """
        Removes a pen from this window.
        
        :param pen: the graphics pen
        :type pen:  ``Pen``
        """
        if pen in self._pencils:
            self._pencils.remove(pen)
        self._mark = True
    
    def _offset(self):
        """
        :return: The drawing offset for the Window canvas
        :rtype:  ``vector``
        """
        from pyx import trafo
        return trafo.trafo(vector=(self.width/2.0,self.height/2.0))
    
    
    # PUBLIC METHODS
    def clear(self):
        """
        Erases the contents of this Window
        
        All Turtles and Pens are eliminated from the Window. Any attempt to use a 
        previously created :class:`Turtle` or :class:`Pen` will fail.
        """
        from pyx import canvas
        from pyx import path
        clippath = path.rect(self.x, self.y, self.width, self.height)
        self._canvas = canvas.canvas([canvas.clip(clippath)])
        self._turtles = []
        self._pencils = []
    
    def bye(self):
        """
        Shuts the graphics Window
        """
        self._turtles = []
        self._pencils = []
        del self._canvas
    
    def stroke(self, path, clr):
        """
        Draws the given path and color as a line.
        
        :param path: The path to draw
        :type path:  ``path``
        
        :param clr: The color to draw
        :type clr:  3d ``tuple``
        """
        from pyx import color
        pclr = color.rgb(clr[0],clr[1],clr[2])
        self._canvas.stroke(path, [pclr, self._offset()])
        self._mark = True
    
    def fill(self, path, clr):
        """
        Draws the given path as a closed shape
        
        :param path: The path to draw
        :type path:  ``path``
        
        :param clr: The color to draw
        :type clr:  3d ``tuple``
        """
        from pyx import color
        pclr = color.rgb(clr[0],clr[1],clr[2])
        self._canvas.fill(path, [pclr, self._offset()])
        self._mark = True
    
    def flush(self):
        """
        Writes out all of the pens and turtles attached to the window.
        """
        # Draw a bounding box
        from pyx import path
        from pyx import text
        r = path.rect(0,0,self.width,self.height)
        self._canvas.stroke(r)
        
        for t in self._turtles:
            t.flush()
        
        for p in self._pencils:
            p.flush()
        
        # Write the title, if we have one
        if not self.title is None:
            self._canvas.text(0,self.height/2.0-30,"{\\Huge %s}" % self.title,
                              [text.halign.boxcenter, self._offset()])
    
    def embed(self, canvas, x=0, y=0):
        """
        Embeds this Window into the parent canvas at position (x,y)
        
        The Window will be scaled according to the current scaling factor
        
        :param canvas: the parent canvas
        :type canvas:  ``canvas``
        
        :param x: window x-coordinate in the parent canvas (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: window y-coordinate in the parent canvas (default 0)
        :type x:  ``int`` or ``float``
        """
        from pyx import trafo
        offset = trafo.trafo(matrix=((self.scale,0),(0,self.scale)), vector=(x,y))
        canvas.insert(self._canvas,[offset])
    
    
    # UNSUPPORTED METHODS
    def beep(self):
        """
        Unsupported method for compatibility
        """
        pass
    
    def iconify(self):
        """
        Unsupported method for compatibility
        """
        pass
    
    def deiconify(self):
        """
        Unsupported method for compatibility
        """
        pass
    
    def setMaxSize(self,width,height):
        """
        Unsupported method for compatibility
        """
        pass
    
    def setMinSize(self,width,height):
        """
        Unsupported method for compatibility
        """
        pass


# TURTLE HELPERS
def is_valid_color(c):
    """
    Determines if ``c`` is a valid color for a Turtle or Pen.
    
    Turtles accept RGB, HSV, strings (for named colors), or tuples.
    
    :param c: a potential color value
    
    :return: True if c is a valid color value.
    :rtype:  ``bool``
    """
    from ..colors import RGB, HSV
    return type(c) in [RGB, HSV, str, tuple]


# Helper function to support colormodel in turtles
def to_valid_color(c):
    """
    Converts a color to the appropriate TKinter representation.
    
    This method allows us to support all color formats, while using a single
    color format for the backend.
    
    For the PyX backend, the unified color is a Tk-supported color value
    
    :param c: the color value
    :type c:  valid color
    
    :return: The given color value, converted to an internal format
    :rtype:  ``str`` or ``tuple``
    """
    from ..colors import RGB, HSV
    try:
        if type(c) == str:
            if c[0] == '#':
                return RGB.CreateWebColor(c).tkColor()
            else:
                return RGB.CreateName(c).tkColor()
        elif (type(c) == RGB or type(c) == HSV):
            return c.tkColor()
        else:
            return c
    except:
        return (0,0,0)


