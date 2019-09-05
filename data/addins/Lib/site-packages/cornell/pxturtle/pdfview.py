"""
An autograder for Turtle assignments.

The autograder does not assign points.  That is handled by an external program.  It 
just formats a PDF that compares student submissions to the correct solution.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""


class PDFView(object):
    """
    An instance is a PDF page grading a single Turtle task
    
    A grader displays the student solution next to the instructor solution. It also 
    provides the student with comments at the bottom of a page.
    
    A grader is only designed for a single task.  Multiple tasks should each have their 
    own grader object.  The grading document will be made up of multiple such graders.
    
    :ivar x: The x-coordinate of the bounding box in the page
    :vartype x: ``int`` or ``float``
    
    :ivar y: The y-coordinate of the bounding box in the page
    :vartype y: ``int`` or ``float``
    
    :ivar width: The width of the bounding box in the page
    :vartype width: ``int`` or ``float`` >= 0
    
    :ivar height: The height of the bounding box in the page
    :vartype height: ``int`` or ``float`` >= 0
    
    :ivar title: The task title for this grader
    :vartype title: ``str``
    
    :ivar page: The PyX page for this property
    :vartype page: ``page``
    
    :ivar submitted: The window object for the student submission
    :vartype submitted: ``Window``
    
    :ivar solution: The window object for the instructor solution
    :vartype solution: ``Window``
    
    :ivar comments: The list of grading comments for the student
    :vartype comments: ``list``
    """
    #PRIVATE ATTRIBUTES:
    #    _canvas: The canvas backing the grader's document page

    
    # MUTABLE PROPERTIES
    @property
    def x(self):
        """
        The x-coordinate of the bounding box in the page
        
        The value defaults to 0.  Changes to this attribute have no effect until the 
        method :meth:`clear` is called.
        
        **invariant**: Value must be a number (``int`` or ``float``)
        """
        return self._x
    
    @x.setter
    def x(self,value):
        assert type(value) in [int,float], '%s is not a number' % repr(value)
        self._x = value
    
    @property
    def y(self):
        """
        The y-coordinate of the bounding box in the page
        
        The value defaults to 0.  Changes to this attribute have no effect until the 
        method :meth:`clear` is called.
        
        **invariant**: Value must be a number (``int`` or ``float``)
        """
        return self._y
    
    @y.setter
    def y(self,value):
        assert type(value) in [int,float], '%s is not a number' % repr(value)
        self._y = value    
    
    @property
    def width(self):
        """
        The width of the bounding box in the page
        
        The value defaults to the width of US Letter.  Changes to this attribute have no 
        effect until the method :meth:`clear` is called.
        
        **invariant**: Value must be a number (``int`` or ``float``) >= 0
        """
        return self._width
    
    @width.setter
    def width(self,value):
        assert type(value) in [int,float], '%s is not a number' % repr(value)
        assert value >= 0,'%s is negative' % repr(value)
        self._width = value
    
    @property
    def height(self):
        """
        The height of the bounding box in the page
        
        The value defaults to the height of US Letter.  Changes to this
        attribute have no effect until the method clear() is called
        
        **invariant**: Value must be a number (``int`` or ``float``) >= 0
        """
        return self._height
    
    @height.setter
    def height(self,value):
        assert type(value) in [int,float], '%s is not a number' % repr(value)
        assert value >= 0,'%s is negative' % repr(value)

        self._height = value
    
    @property
    def title(self):
        """
        The task title for this grader
        
        **invariant**: Value is a ``str``
        """
        return self._title
    
    @title.setter
    def title(self,value):
        assert type(value) == str, '%s is not a string' % repr(value)
        self._title = value
    
    
    # IMMUTABLE PROPERTIES
    @property
    def page(self):
        """
        The PyX page for this property
        
        This object is used to embed the grader into a document.
        
        **invariant**: Value is a PyX page (not None)"""
        return self._page
    
    @property
    def submitted(self):
        """
        The window object for the student submission
        
        **invariant**: Value is a ``Window`` (not None)
        """
        return self._submitted
    
    @property
    def solution(self):
        """
        The window object for the instructor solution
        
        **invariant**: Value is a`` Window`` (not None)
        """
        return self._solution
    
    @property
    def comments(self):
        """
        The list of grading comments for the student
        
        **invariant**: Value is a (possibly empty) list of ``str``
        """
        return self._comments
    
    # BUILT-IN METHODS
    def __init__(self,title='',x=0,y=0,width=612,height=792):
        """
        Creates a new grader for a single Turtle task.
        
        :param title: the task title (default '')
        :type title:  ``str``
        
        :param x: the x-coordinate of the PDF bounding box (default 0)
        :type x:  ``int`` or ``float``
        
        :param y: the y-coordinate of the PDF bounding box (default 0)
        :type y:  ``int`` or ``float``
        
        :param width: the width of the PDF bounding box (default US Letter)
        :type width:  ``int`` or ``float`` >= 0
        
        :param height: the height of the PDF bounding box (default US Letter)
        :type height:  ``int`` or ``float`` >= 0
        
        :param position: initial pen position (origin is screen center)
        :type position: 2D ``tuple``
        """
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        self.title  = title
        self._pglist = []
        self.clear()
    
    def clear(self):
        """
        Clears the grader, creating all new canvases for drawing.
        """
        from pyx import canvas
        from pyx import bbox
        from pyx import document
        from .window import Window
        
        self._canvas = canvas.canvas()
        bounds = bbox.bbox(self.x,self.y,self.width,self.height)
        self._page = document.page(self._canvas,
                                   paperformat=document.paperformat.Letter,
                                   bbox=bounds)
        self._submitted = Window()
        self._submitted.title = 'Student Submission'
        self._solution  = Window()
        self._solution.title = 'Instructor Solution'
        self._comments = []
    
    def append(self,mssg):
        """
        Appends a grading comment to this grader.
            
        :param mssg: a grading comment
        :type mssg:  ``str``
        """
        self._comments.append(mssg)
    
    def flush(self):
        """
        Writes all graphics to the page, preparing it for output.
        
        This method also clears the canvas to allow it to be reused.
        
        This method draws the student and instructor submissions at the top, and places 
        the grading comments below
        """
        from pyx import text
        # Determine the margins relative to US letter
        bdx = max(self.x,36)
        bdy = max(self.y,36)
        bdw = min(self.width,540)
        bdh = min(self.height,720)
        
        xoff = (self.width-bdw)/2.0
        
        self.submitted.flush()
        self.submitted.scale = 0.45
        yoff = (self.height-bdy-self.submitted.height*self.submitted.scale)
        self.submitted.embed(self._canvas,x=xoff,y=yoff)
        self.solution.flush()
        self.solution.scale = 0.45
        yoff = (self.height-bdy-self.solution.height*self.solution.scale)
        self.solution.embed(self._canvas,x=self.width/2.0,y=yoff)
        
        header = 'Autograder Comments' if self.title == '' else 'Autograder Comments on '+self.title
        self._canvas.text(bdx,self.height/2.0,"{\\Large\\textbf{%s}:} " % header)
        
        # Internal offset for comments
        yoff = self.height/2.0-30
        
        # Add the comments
        body = "\large\\noindent "
        frst = True
        for line in self._comments:
            if frst:
                frst = False
            else:
                body += " \\\\"
            body += line
        self._canvas.text(xoff,yoff,body,[text.parbox(bdw)])
        
        # Store canvas in page list and clear
        self._pglist.append(self._page)
        self.clear()
    
    def write(self,fname):
        """
        Writes this grader out to a PDF file
        
        :param fname: the PDF file to produce
        :type fname:  ``str``
        """
        from pyx import document
        docs = document.document(pages=self._pglist)
        docs.writePDFfile(fname)


