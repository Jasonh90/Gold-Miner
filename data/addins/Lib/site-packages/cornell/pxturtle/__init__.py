"""
PyX backend to the Tk Turtle

This is an attempt to speed up grading of the TkTurtle assignment. It replaces the Tcl/Tk 
backend with PyX, which creates a PDF of the output.

Author: Walker M. White (wmw2)
Date:   July 13, 2017 (Python 3 version)
"""
from pyx import unit
from pyx import text

unit.set(defaultunit='pt')
text.set(cls=text.LatexRunner)

from .pdfview import PDFView
from .window import Window
from .turtle import Turtle
from .pen import Pen
