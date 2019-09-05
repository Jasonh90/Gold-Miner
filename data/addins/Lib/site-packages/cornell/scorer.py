"""
Module to simplify autograders

I am on record as saying that there is no such thing as a useful third-party autograder.
All grading should be tailored to the assignment or problem.  However, it is useful to
have a tool that can record and tabulate grades, as well as gather feedback.  That is
what this tool does.

Author: Walker M. White
Date:   July 20, 2017
"""
import sys, traceback
import numpy
import types


def _format_score(score,prev,maxv):
    """
    Returns the score formatted for alignment.
    
    The score is padded so that numbers align at the ones digit.
    
    :param score: The raw score as a string
    :type score:  ``str``
    
    :param prev: The position of the ones digit in the string
    :type prev:  ``int``
    
    :param maxv: The number of spaces to pad out the string to
    :type maxv:  ``int``
    
    :return: the score formatted for alignment.
    :rtype:  ``str``
    """
    pos = score.find('.')
    if pos == -1:
        pos = len(score)
    
    remp = len(score)-pos
    diff = maxv-prev
    return ' '*(prev-pos)+score+' '*(diff-remp)


def _rowlen(y):
    """
    Returns a function to compute the length of a table row
    
    The function allows us to map len to 2-dimensional sequence. The attribute ``y``
    selects row position.
    
    :param y: The row position
    :type y:  ``int``
    
    :return: a function to compute the length of table row ``y``
    :rtype:  ``callable``
    """
    return lambda x : len(x[y])


def _rowdot(y):
    """
    Returns a function to find the decimal point in a table row.
    
    This function allows us to map ``find('.')`` to a list of strings.  The attribute
    ``y`` selects the row position.  The returned function will return the row length
    if there is no '.'.
    
    :param y: The row position
    :type y:  ``int``
    
    :return: a function to find the decimal point in table row ``y``
    :rtype:  ``callable``
    """
    return lambda x : x[y].find('.') if '.' in x[y] else len(x[y])


class Scorer(object):
    """
    An instance is object for tallying scores and providing feedback.
    
    This class is not a proper autograder.  Instead, it is a framework to attach
    autograders.  Those graders, then use this object to deduct points and provide
    feedback.  When done, this object can print out a score sheet.
    
    When attaching graders to the scorer, you can either attach a callback function
    or a list.  If you attach a callback function, it will use that function as
    the grader.  If you attach a list, it will assume that these are all subparts of
    the problem.  Those subparts should then attach to either a callback (to grade)
    or another list (for more subparts).
    
    :ivar _title: The title of this assignment (for display in the report)
    :vartype _title: ``str``
    
    :ivar _indent: The current indentation level (for message display)
    :vartype _indent: ``int``
    
    :ivar _cursor: The current problem being graded
    :vartype _cursor: ``str``
    """
    @property
    def title(self):
        """
        The title of this assignment.
        
        This is displayed by the method :meth:`report` when providing feedback.
        
        **invariant**: Value is a ``str``
        """
        return self._title
    
    @title.setter
    def title(self,value):
        assert type(value) == str, '%s is not a string' % repr(value)
        self._title = value
    
    @property
    def indent(self):
        """
        The current indentation level.
        
        When a message is sent by a grader function via :meth:`message`, :meth:`deduct`
        or one of the assert methods, it will be indented by this amount. Negative
        values will not indent.
        
        **invariant**: Value is an ``int``
        """
        return self._indent
    
    @indent.setter
    def indent(self,value):
        assert type(value) == int, '%s is not an int' % repr(value)
        self._indent = value
    
    @property
    def current(self):
        """
        The current problem being graded.
        
        While the autograder callbacks are running, they sometimes need to know what
        the current problem is (e.g. to retrieve the maximum score).  This value makes
        it possible.  If grading is not in progress, this value is ``None``.
        
        **invariant**: Value is ``str`` or ``None``
        """
        return self._cursor
    
        
    def __init__(self, name):
        """
        Creates a Scorer for the given assignment.
        
        This new Scorer will have no problems to score. Those must be attached individually
        with the :meth:`attach` method.
        
        :param name: The name of the assignment
        :type name:  ``str``
        """
        self.title = name
        self._cursor = None
        self._roots  = []
        self._allkey = {}
        self._totals = {}
        self._scores = {}
        self._childs = {}
        self._master = {}
        self._output = []
        self._indent = 0
    
    def reset(self):
        """
        Resets the scorer, erasing all feedback and deductions.
        """
        self._cursor = None
        for name in self._totals:
            self._scores[name] = self._totals[name]
        self._output = []
        self.indent = -2
    
    def attach(self,name,child,points=None,mastery=False):
        """
        Attaches a problem grader to this scorer.
        
        The value ``name`` should be a unique name identifying the problem to grade.
        It is then associated with ``child`` that performs the grading.
        
        The values ``child`` should either be a callback function or a list.  If it is
        a callback function, then it should take a scorer as an argument.  That way,
        the callback function can use this object to provide feedback and deduct points.
        The value ``points`` is the maximum number of points that can be deducted.
        
        On the other hand, if ``child`` is a list or tuple, then that sequence should
        consist of names of subparts to grade.  Each subpart must be attached 
        individually.  Those subparts will have their own associated points.  For
        this parent problem ``points`` refers to the number of parts that must be
        completed (for cases of "best x out of y").
        
        Finally, the value ``mastery`` only applies when ``child`` is a sequence of 
        subparts.  It indicates that any loss of points on one part will prevent the
        scorer from going on to the next part in the grading process.
        
        :param name: The unique problem name
        :type name:  ``str``
        
        :param child: The grader or sequence of subproblems
        :type child:  ``callable`` or ``iterable``
        
        :param points: The maximum number of points for this problem (or subproblems to grade)
        :type points:  ``int`` or ``float`` >= 0
        
        :param mastery: Whether or not mastery is required for this problem.
        :type mastery:  ``bool``
        """
        assert type(name) == str, '%s is not a string' % repr(name)
        assert points is None or type(points) in [int,float], '%s is not an number' % repr(points)
        assert points is None or points >= 0, '%s is negative' % repr(points)
        assert type(mastery) == bool, '%s is not a bool' % repr(mastery)
        
        if not name in self._allkey:
            self._roots.append(name)
            self._allkey[name] = True
        self._childs[name] = child
        self._master[name] = mastery
        
        if not (child is None or callable(child)):
            if points is None:
                points = len(child)
            
            assert type(points) == int, '%s is not an int' % repr(points)
            assert points >= 0 and points <= len(child), '%s is not in range' % repr(points)
            
            for item in child:
                assert type(name) == str, '%s is not a string' % repr(name)
                self._allkey[item] = True
        elif points is None:
            points = 0
        
        self._totals[name] = points
        self._scores[name] = points
    
    def maximum(self,name=None):
        """
        Returns the maximum score for the given problem.
        
        If ``name`` refers to a list of problems, it totals the score for that list
        (taking "best x out of y" as appropriate).  If ``name`` is ``None``, it provides
        the score on the entire assignment.
        
        :param name: The problem to score
        :type name:  ``str`` or ``None``
        
        :return: the maximum score for the given problem
        :rtype:  ``int`` or ``float``
        """
        if name is None:
            keyset = self._roots
            requir = len(self._roots)
        elif name in self._childs:
            keyset = self._childs[name]
            requir = self._totals[name]
        else:
            return 0
        
        if keyset is None or callable(keyset):
            return self._totals[name]
        else:
            scores = []
            for item in keyset:
                scores.append(self.maximum(item))
            scores.sort()
            
            result = 0
            for i in range(requir):
                result += scores[i]
            return result
    
    def score(self,name=None):
        """
        Returns the current score for the given problem.
        
        If ``name`` refers to a list of problems, it totals the score for that list
        (taking "best x out of y" as appropriate).  If ``name`` is ``None``, it provides
        the score on the entire assignment.
        
        :param name: The problem to score
        :type name:  ``str`` or ``None``
        
        :return: the current score for the given problem
        :rtype:  ``int`` or ``float``
        """
        if name is None:
            keyset = self._roots
            requir = len(self._roots)
        elif name in self._childs:
            keyset = self._childs[name]
            requir = self._totals[name]
        else:
            return 0
        
        if keyset is None or callable(keyset):
            return self._scores[name]
        else:
            scores = []
            for item in keyset:
                scores.append(self.score(item))
            scores.sort()
            
            result = 0
            for i in range(requir):
                result += scores[-(i+1)]
            return result
    
    def grade(self,name=None):
        """
        Invokes the autograder(s) attached to the given problem.
        
        It ``name`` is mapped to a callback, this function invokes that callback.
        If ``name`` is mapped to a list of problems, it grades all of those problems
        (which may have further nesting).  If ``name`` is None, it grades the entire
        assignment using all attached autograders.
        
        :param name: The problem to grade
        :type name:  ``str`` or ``None``
        """
        if name is None:
            self.reset()
            keyset = self._roots
            message = 'Start grading of '+self._title+'\n'
            master  = False
        elif name in self._childs:
            keyset = self._childs[name]
            master = self._master[name]
            maxpts = self.maximum(name)
            if master:
                message = 'Grading '+name
            else:
                message = 'Max points for '+name+': '+str(maxpts)
        else:
            keyset = None
        
        if not keyset:
            return True
        
        self._cursor = name
        self._output.append((' '*self._indent)+message)
        self._indent += 2
        
        iterate = not callable(keyset)
        if iterate:
            for item in keyset:
                self.grade(item)
                if master and self.score(item) != self.maximum(item):
                    break
        else:
            try:
                keyset(self)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                message = 'INTERNAL ERROR: grader for '+name+' crashed'
                self._output.append((' '*self._indent)+message)
                self._output.append(traceback.format_exception_only(exc_type,exc_value)[0])
                self._output.append(traceback.format_exc()[:-1])
                self._scores[name] = 0
        
        self._indent -= 2
        if not name is None:
            self._output.append((' '*self._indent)+'Finished '+name)
            self._output.append('')
    
    def message(self,msg):
        """
        Appends a message to the feedback list for this scorer.
        
        The message will have the current indentation.
        
        :param msg: The feedback message to display
        :type msg:  ``str``
        """
        assert not self._cursor is None, 'The scorer is not actively grading'
        assert type(msg) == str, '%s is not a string' % msg
        self._output.append((' '*self._indent)+msg)
    
    def deduct(self, msg, amt):
        """
        Deducts points from the current problem and adds a feedback message.
        
        The deduction will be take from the current problem. Deduction will only occur 
        if the maximum deduction has not been reached yet.  Unless the problem is for
        mastery (in which case any deduction is bad), the feedback will include the 
        number of points deducted.
        
        The message will display before the deduction feedback.  It will have the current 
        indentation.
        
        :param msg: The feedback message to display
        :type msg:  ``str``
        
        :param amt: The number of points to deduct.
        :type amt:  ``int`` or ``float``
        """
        assert not self._cursor is None, 'The scorer is not actively grading'
        assert type(msg) == str, '%s is not a string' % msg
        assert type(amt) in [int,float], '%s is not a number' % amt
        
        name = self._cursor
        master = self._master[name]
        
        if self._scores[name] == 0:
            if not master:
                msg += ' Maximum deduction reached.'
            self._output.append((' '*self._indent)+msg)
            return 0
        else:
            pts = min(amt,self._scores[name])
            if not master:
                suff = ' point' if pts == 1 else ' points'
                msg += ' '+str(pts)+suff+' deducted.'
            self._output.append((' '*self._indent)+msg)
            self._scores[name] -= pts
            return pts
    
    def check_equals(self, msg, answer, given, amt):
        """
        Deducts points if answer != given
        
        This problem is written to work with either floats or standard equality. 
        The feedback message will used ``msg`` as its prefix to put the two values
        in context.  For example, if ``msg`` is 'Variable x is', ``answer`` is 2
        and ``given`` is 1, the feedback message will be::
            
            'Variable x is 1 but should be 2'
        
        The deduction will be take from the current problem. Deduction will only occur 
        if the maximum deduction has not been reached yet.  Unless the problem is for
        mastery (in which case any deduction is bad), the feedback will include the 
        number of points deducted.
        
        The message will display before the deduction feedback.  It will have the current 
        indentation.
        
        :param msg: The feedback prefix
        :type msg:  ``str``
        
        :param answer: The expected answer
        :type answer:  any
        
        :param given: The student answer
        :type given:  any
        
        :param amt: The number of points to deduct.
        :type amt:  ``int`` or ``float``
        """
        assert type(msg) == str, '%s is not a string' % msg
        try:
            notsame = not numpy.allclose([answer],[given])
        except:
            notsame = answer != given
        
        if notsame:
            explain = msg + ' ' + repr(given) + ' but should be ' + repr(answer) + '.'
            self.deduct(explain,amt)
    
    def check_different(self, msg, answer, given, amt):
        """
        Deducts points if answer == given
        
        This problem is written to work with either floats or standard equality. 
        The feedback message will used ``msg`` as its prefix to put the two values
        in context.  For example, if ``msg`` is 'Variable x is', ``answer`` is 2
        and ``given`` is 1, the feedback message will be::
            
            'Variable x is 1 but should be 2'
        
        The deduction will be take from the current problem. Deduction will only occur 
        if the maximum deduction has not been reached yet.  Unless the problem is for
        mastery (in which case any deduction is bad), the feedback will include the 
        number of points deducted.
        
        The message will display before the deduction feedback.  It will have the current 
        indentation.
        
        :param msg: The feedback prefix
        :type msg:  ``str``
        
        :param answer: The expected answer
        :type answer:  any
        
        :param given: The student answer
        :type given:  any
        
        :param amt: The number of points to deduct.
        :type amt:  ``int`` or ``float``
        """
        assert type(msg) == str, '%s is not a string' % msg
        try:
            same = numpy.allclose([answer],[given])
        except:
            same = answer = given
        
        if same:
            explain = msg + ' expected something different from ' + repr(answer) + '.'
            self.deduct(explain,amt)
    
    def check_copy(self, msg, answer, given, amt):
        """
        Deducts points if answer != given or answer IS given
        
        This problem is written to work with either floats or standard equality. 
        The feedback message will used ``msg`` as its prefix to put the two values
        in context.  For example, if ``msg`` is 'Variable x is', ``answer`` is 2
        and ``given`` is 1, the feedback message will be::
            
            'Variable x is 1 but should be 2'
        
        The deduction will be take from the current problem. Deduction will only occur 
        if the maximum deduction has not been reached yet.  Unless the problem is for
        mastery (in which case any deduction is bad), the feedback will include the 
        number of points deducted.
        
        The message will display before the deduction feedback.  It will have the current 
        indentation.
        
        :param msg: The feedback prefix
        :type msg:  ``str``
        
        :param answer: The expected answer
        :type answer:  any
        
        :param given: The student answer
        :type given:  any
        
        :param amt: The number of points to deduct.
        :type amt:  ``int`` or ``float``
        """
        """If answer = given, add score to total otherwise, append error msg to output"""
        assert type(msg) == str, '%s is not a string' % msg
        try:
            notsame = not numpy.allclose([answer],[given])
        except:
            notsame = answer != given
        
        if notsame:
            explain = msg + ' ' + repr(given) + ' but should be ' + repr(answer) + '.'
            self.deduct(explain,amt)
        elif id(answer) == id(given):
            explain = msg + ' did not copy ' + repr(answer) + '.'
            self.deduct(explain,amt)
    
    def tally(self):
        """
        Prints out a tally sheet of the scores on each problem.
        
        Currently the tally sheet only does one level of nesting. If you have subsubparts,
        it will only show the total for the parent parts.
        """
        contents = self._gather_lines()
        
        # We need to compare the scores to line them up.
        maxlen = max(map(_rowlen(0),contents.values())) if contents else 0
        maxscr = max(map(_rowlen(1),contents.values())) if contents else 0
        maxmax = max(map(_rowlen(2),contents.values())) if contents else 0
        prescr = max(map(_rowdot(1),contents.values())) if contents else 0
        premax = max(map(_rowdot(2),contents.values())) if contents else 0
        
        # Reformat the numbers
        for name in contents:
            contents[name][1] = _format_score(contents[name][1],prescr,maxscr)
            contents[name][2] = _format_score(contents[name][2],premax,maxmax)
        
        self._print_lines(contents,maxlen)
        
        # Add the final score
        print('-'*(maxlen))
        score = str(self.score())
        maxim = str(self.maximum())
        for name in ['__pretotal__','__deductions__','__total__']:
            maxim = contents[name][2]
            suff  = (contents[name][1]+' out of '+maxim) if maxim.strip() != '' else ''
            pref  = contents[name][0]
            report = pref+' '*(maxlen-len(pref))+suff
            print(report)
    
    def _gather_lines(self):
        """
        Returns a dictionary of the unaligned tally sheet.
        
        For each problem, the dictionary contains a three tuple of the row text,
        the current score, and the maximum score.  These will be pasted to gether
        to produce a line of the tally sheet after the numbers are aligned properly.
        
        :return: a dictionary of the unaligned tally sheet.
        :rtype:  ``dict``
        """
        contents = {}
        index = 1
        for name in self._roots:
            value = str(index)+'. '+name
            try:
                # This only succeeds if we have a sublisting
                if self._totals[name] != len(self._childs[name]):
                    value += ' (Best '+str(self._totals[name])+' out of '+str(len(self._childs[name]))+')'
                subindex = 1
                for item in self._childs[name]:
                    pref = chr(64+subindex)+'. '
                    score = str(self.score(item))
                    maxim = self.maximum(item)
                    maxim = str(maxim) if maxim > 0 else ''
                    contents[item] = ['   '+pref+item+'   ',score,maxim]
                    subindex += 1
            except:
                pass
            score = str(self.score(name))
            maxim = self.maximum(name)
            maxim = str(maxim) if maxim > 0 else ''
            contents[name] = [value+'   ', score, maxim]
            index += 1
        
        contents['__pretotal__'] = ['Total',str(self.score()),str(self.maximum())]
        contents['__deductions__'] = ['Deductions:','','']
        contents['__total__']    = ['Total','',str(self.maximum())]
        
        return contents
    
    def _print_lines(self,contents,maxlen):
        """
        Glues together the results of :meth:`_gather_lines` to produce the tally sheet.
        
        The score numbers should be padded to alignment before calling this method.
        
        :param contents: The results of :meth:`_gather_lines`, with numbers aligned.
        :type contents:  ``dict``
        
        :param maxlen: The maximum line length of any line (to define padding)
        :type maxlen:  ``int``
        """
        for name in self._roots:
            maxim = contents[name][2]
            suff  = (contents[name][1]+' out of '+maxim) if maxim.strip() != '' else ''
            pref  = contents[name][0]
            report = pref+' '*(maxlen-len(pref))+suff
            print(report)
            try:
                for item in self._childs[name]:
                    pref = contents[item][0]
                    line = pref+' '*(maxlen-len(pref))
                    line = line[:-1]+'('+contents[item][1]+')'
                    print(line)
            except:
                pass
    
    def report(self,tally=True):
        """
        Prints out a report of the student's performance with feedback.
        
        If ``tally`` is true, it will include a scoresheet.  Otherwise, it will assume
        that the assignment was for feedback only and simply indicate whether or not
        revisions are necessary.
        
        :param tally: Whether to include a scoresheet
        :type tally:  ``bool``
        """
        self._cursor = None
        print('\n'.join(self._output))
        
        if tally:
            self.tally()
        else:
            if self.score() == self.maximum():
                print('Assignment is complete')
            else:
                print('This assignment requires revisions')


class UnitChecker(object):
    """
    An instance is a verifier for student unit tests.
    
    A checker is assigned to a single function begin tested.  If a unit test actually
    involves more than one function (as is the case in Assignment 1), then the unit
    test grader will need a checker for each individual function.
    
    The unit checker wraps the function being tested with a provided hash function.
    This allows us to count the number of valid unit tests.  The hash function should
    have exactly the same signature as the function being tested.
    
    The grader should use the :meth:`report` method to display the results.
    
    :ivar _name: The function name
    :vartype _name: ``str``
    
    :ivar _hash: The hash function for counting valid tests
    :vartype _hash: ``callable``
    
    :ivar _need: The number of valid tests required to be correct
    :vartype _need: ``int``
    
    :ivar _count: The number of valid tests recorded so far
    :vartype _count: ``int``
    
    :ivar _soln: The module with the solution function
    :vartype _soln: ``module`` or ``None``
    
    :ivar _orig: The original, unwrapped function (if currently wrapped)
    :vartype _orig: ``callable`` or ``None``
    """
    
    @property
    def name(self):
        """
        The function name as a string.
        
        This name allows us to apply the checker to any module that implements this
        function.
        
        **invariant**: This value is set at creation and cannot be changed.
        """
        return self._name
    
    @property
    def needed(self):
        """
        The number of valid tests required to be correct
        
        **invariant**: Value is an ``int``
        """
        return self._need
    
    @needed.setter
    def needed(self,value):
        assert type(value) == int, '%s is not an integer' % repr(value)
        assert value >= 0, '%s is not nonnegative' % repr(value)
        self._need = value
    
    @property
    def solution(self):
        """
        The module containing the solution to this function.
        
        If there is a solution module, then wrapping a function will replace it entirely 
        with the version in the solution.  Otherwise, the :meth:`wrap` method will assume
        the function being tested is correct and wrap it in place.
        
        **invariant**: Value is an ``module`` or ``None``
        """
        return self._soln
    
    @needed.setter
    def solution(self,value):
        assert value is None or type(value) == types.ModuleType, '%s is not an module' % repr(value)
        self._soln = value
    
    @property
    def found(self):
        """
        The number of valid tests found so far.
        
        The method :meth:`reset` will reset this value to 0.  To record tests, wrap the
        function and call the unit test function.
        
        **invariant**: Value is an ``int`` >= 0
        """
        result = 0
        for key in self._count:
            if key >= 0:
                result += 1
        return result
    
    @property
    def invalid(self):
        """
        The number of invalid tests (those that violate the precondition)
        
        The method :meth:`reset` will reset this value to 0.  To record tests, wrap the
        function and call the unit test function.
        
        **invariant**: Value is an ``int`` >= 0
        """
        result = 0
        for key in self._count:
            if key < 0:
                result += 1
        return result
    
    def __init__(self,name,hash,need=0,soln=None):
        """
        Creates a UnitChecker for the given function and hash.
        
        If there is a solution module, then wrapping a function will replace it entirely 
        with the version in the solution.  Otherwise, the :meth:`wrap` method will assume
        the function being tested is correct and wrap it in place.
        
        :param name: The function name
        :type name:  ``str``
        
        :param hash: The hash function for counting valid tests
        :type hash:  ``callable``
        
        :param need: The number of valid tests required to be correct
        :type need:  ``int``
        
        :param _soln: The module with the solution function
        :type _soln:  ``module`` or ``None``
        """
        assert type(name) == str, '%s is not a string' % repr(name)
        assert callable(hash), '%s is not callable' % repr(hash)
        self._name = name
        self._hash = hash
        self.needed   = need
        self.solution = soln
        self._orig = None
        self._count = set()
    
    def wrap(self,parent):
        """
        Wraps the implementation of ``name`` in the module ``parent``
        
        When a function is wrapped, any future calls to it will be recorded by the
        hash function.
        
        :param parent: The module with the function
        :type parent:  ``module``
        """
        assert type(parent) == types.ModuleType, '%s is not an module' % repr(parent)
        try:
            self._orig = getattr(parent,self._name)
            src = self._soln if self._soln else parent
            src = getattr(src,self._name)
            dst = lambda *x : (self._count.add(self._hash(*x)),src(*x))[1]
            setattr(parent,self._name,dst)
        except:
            pass
    
    def unwrap(self,parent):
        """
        Unwraps the implementation of ``name`` in the module ``parent``
        
        When a function is unwrapped, it is restored to its original version, and calls
        will no longer be recorded by the hash function.
        
        :param parent: The module with the function
        :type parent:  ``module``
        """
        assert type(parent) == types.ModuleType, '%s is not an module' % repr(parent)
        try:
            setattr(parent,self._name,self._orig)
        except:
            pass
    
    def reset(self):
        """
        Resets the checker, erasing all recorded calls.
        """
        self._count = set()
    
    def report(self,scorer):
        """
        Reports the success of the unit test to the :class:`Scorer` object
        
        We assume that one point is deducted for each test case missing.
        
        :param scorer: The object recording the student's score.
        :type scorer:  :class:`Scorer`
        """
        if self.invalid > 0:
            suff = ' test ' if self.invalid == 1 else ' tests '
            scorer.deduct('You have '+self.invalid+suff+'that violate the precondition',self.invalid)
        
        if self.found == 0:
            print(self.needed)
            print(self._orig)
            scorer.deduct('There were no tests for '+self._name+'.',self.needed)
        elif self.found < self.needed-1:
            miss = self.needed-self.found
            scorer.deduct('You are missing '+repr(miss)+' tests for '+self._name+'.',miss)
        elif self.found == self.needed-1:
            scorer.deduct('You are missing an important test for '+self._name+'.',1)


