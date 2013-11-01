
 
#  Copyright (c) 2005 Gavin E. Crooks <gec@threeplusone.com>
#
#  This software is distributed under the MIT Open Source License.
#  <http://www.opensource.org/licenses/mit-license.html>
#
#  Permission is hereby granted, free of charge, to any person obtaining a 
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
#  THE SOFTWARE.
#


"""Extra utilities and core classes not in standard python.
"""


__all__ = ('isblank', 'isfloat', 'isint', 'fcmp', 'remove_whitespace', 
            'invert_dict','update', 'stdrepr', 'Token', 'Struct', 'Reiterate',
             'deoptparse', 'crc32', 'crc64', 'FileIndex', 'find_command',
             'ArgumentError', 'frozendict')

import os.path
import math

def isblank( string) :
    """Is this whitespace or an empty string?"""
    if string == '' : return True
    return string.isspace()

def isfloat(s):
    """Does this object represent a floating point number? """
    try: 
        float(s)
        return True
    except (ValueError, TypeError): 
        return False

def isint(s):
    """Does this object represent an integer?"""
    try: 
        int(s)
        return True
    except (ValueError, TypeError): 
        return False
        
def fcmp(x, y, precision):
    """Floating point comparison."""
    # TODO: Doc string, default precision. Test
    if math.fabs(x-y) < precision:
        return 0
    elif x < y:
        return -1
    return 1

def remove_whitespace( astring) :
    """Remove all whitespace from a string."""
    # TODO: Is this horrible slow?   
    return "".join(astring.split())


def invert_dict( dictionary) :
    """Constructs a new dictionary with inverted mappings so that keys become 
    values and vice versa. If the values of the original dictionary are not
    unique then only one of the original kesys will be included in the new
    dictionary.
    """
    return dict( [(value, key) for key, value in dictionary.iteritems()] )



def update(obj, **entries):
    """Update an instance with new values. 

    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    """
    if hasattr(obj, 'update') :
        obj.update( entries) 
    else :
        for k, v in entries.iteritems() :
            setattr(obj, k, v)
    return obj



def stdrepr( obj,  attributes=None, name=None) :
    """Create a standard representation of an object."""
    if name==None : name = obj.__class__.__name__
    if attributes==None: attributes = obj.__class__.__slots__
    args = []
    for a in attributes :
        args.append( '%s=%s' % ( a, repr( getattr(obj, a) ) ) )
    args = ',\n'.join(args).replace('\n', '\n    ')
    return '%s(\n    %s\n)' % (name, args)
   

class Token(object):
    """Represents the items returned by a file scanner, normally processed
    by a parser.
    
    Attributes :
    o typeof    -- a string describing the kind of token
    o data      -- the value of the token
    o lineno    -- the line of the file on which the data was found (if known)
    o offset    -- the offset of the data within the line (if known)
    """
    __slots__ = [ 'typeof', 'data', 'lineno', 'offset']
    def __init__(self, typeof, data=None, lineno=-1, offset=-1) :
        self.typeof = typeof
        self.data = data
        self.lineno = lineno
        self.offset = offset
 
    def __repr__(self) :
        return stdrepr( self) 

    def __str__(self):
        coord = str(self.lineno)
        if self.offset != -1 : coord += ':'+str(self.offset)
        coord = coord.ljust(7)
        return (coord+ '  '+ self.typeof +' : ').ljust(32)+ str(self.data or '')



def Struct(**kwargs) :
    """Create a new instance of an anonymous class with the supplied attributes
    and values.
    
    >>> s = Struct(a=3,b=4)
    >>> s
    Struct(
        a=3,
        b=4
    )
    >>> s.a
    3
    
    """
    name = 'Struct'
    
    def _init(obj,  **kwargs) :
        for k, v in kwargs.iteritems() :
            setattr( obj, k, v)
    
    def _repr(obj) :
        return stdrepr( obj,  obj.__slots__, name)

    adict = {}
    adict['__slots__'] = kwargs.keys()
    adict['__init__'] = _init
    adict['__repr__'] = _repr
    
    return type( name, (object,) , adict)(**kwargs)
    

class Reiterate(object):
    """ A flexible wrapper around a simple iterator.    
    """
    def __new__(cls, iterator):
        if isinstance(iterator, cls) : return iterator
        new = object.__new__(cls)
        new._iterator = iter(iterator)
        new._stack = []
        new._index = 0 
        return new

    def __init__(self, *args, **kw):
        pass   

            
    def __iter__(self):
        return self
        
    def next(self): 
        """Return the next item in the iteration."""
        self._index +=1
        if self._stack : 
            return self._stack.pop()
        else: 
            return self._iterator.next()

    def index(self) :
        """The number of items returned. Incremented by next(), Decremented
        by push(), unchanged by peek()  """
        return self._index
        
    def push(self, item) :
        """Push an item back onto the top of the iterator,"""
        self._index -=1
        self._stack.append(item)
        
    def peek(self) :
        """Returns the next item, but does not advance the iteration.
        Returns None if no more items. (Bit may also return None as the
        next item.)"""
        try :
            item = self.next()
            self.push(item)
            return item
        except StopIteration:
            return None

    def has_item(self) :
        """More items to return?"""
        try :
            item = self.next()
            self.push(item)
            return True
        except StopIteration:
            return False    
            
    def filter(self, predicate):
        """Return the next item in the iteration that satisifed the 
        predicate."""
        next = self.next()
        while not predicate(next) : next = self.next()
        return next
# End class Reiterate





def crc32(string):
    """Return the standard CRC32 checksum as a hexidecimal string."""
    import binascii
    return "%08X"% binascii.crc32(string)

_crc64_table =None

def crc64(string):
    """ Calculate ISO 3309 standard cyclic redundancy checksum.
    Used, for example, by SWISS-PROT.
    
    Returns : The CRC as a hexadecimal string.
    
    Reference: 
    o W. H. Press, S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery,
     "Numerical recipes in C", 2nd ed., Cambridge University Press. Pages 896ff.
    """
    # Adapted from biopython, which was adapted from bioperl
    global _crc64_table
    if _crc64_table is None :
        # Initialisation of CRC64 table
        table = []
        for i in range(256):
            l = i
            part_h = 0
            for j in range(8):
                rflag = l & 1
                l >>= 1
                if part_h & 1: l |= (1L << 31)
                part_h >>= 1L
                if rflag: part_h ^= 0xd8000000L
            table.append(part_h)
        _crc64_table= tuple(table)
    
    crcl = 0
    crch = 0
    for c in string:
        shr = (crch & 0xFF) << 24
        temp1h = crch >> 8
        temp1l = (crcl >> 8) | shr
        idx  = (crcl ^ ord(c)) & 0xFF
        crch = temp1h ^ _crc64_table[idx]
        crcl = temp1l

    return "%08X%08X" % (crch, crcl)
# End crc64


class FileIndex(object) :
    """Line based random access to a file. Quickly turn a file into a read-only
    database.
    
    Attr:
    - indexfile -- The file to be indexed. Can be set to None and latter
                replaced with a new file handle, for exampel, if you need to
                close and latter reopen the file. 
    
    Bugs:
        User must set the indexedfile to None before pickling this class.  
    
    """
    __slots__ = [ 'indexedfile', '_parser', '_positions', '_keys', '_key_dict']
    
    def __init__(self, indexedfile, linekey = None, parser=None) :
        """
            
        Args:
        - indexedfile -- The file to index
        - linekey -- An optional function. keyofline() will be passed each line
            of the file in turn and should return a string to index the line, 
            or None. If keyofline() is supplied, then only lines that generate  
            keys are indexed.
        - parser -- An optional parser. A function that reads from a file handle
            positioned at the start of a record and returns an object.   
        """
    
        def default_parser(seekedfile) :
            return seekedfile.readline()
            
        if parser is None : parser = default_parser
        self._parser = parser
        
        indexedfile.seek(0)
        positions = []
        keys = []
        
        while True :
            position = indexedfile.tell()
            line = indexedfile.readline()
            if line == '' : break    
            
            if linekey :
                k = linekey(line)
                if k is None: continue
                keys.append(k)

            positions.append(position)
        
        self.indexedfile = indexedfile
        self._positions = tuple(positions)
        
        if linekey :
            self._keys = tuple(keys)
            self._key_dict = dict( zip(keys, positions))

        
    def tell(self, item) :
        if isinstance(item, str) : 
            p = self._key_dict[item]
        else :
            p = self._positions[item]
        return p
        
    def seek(self, item) :
        """Seek the indexfile to the position of item."""
        self.indexedfile.seek(self.tell(item))
    
    def __iter__(self) :
        for i in range(0, len(self)) :
            yield self[i]
                
    def __len__(self) :
        return len(self._positions)
         
    def __getitem__(self, item) :
        self.indexedfile.seek(self.tell(item))
        return self._parser(self.indexedfile)
    
    def __contains__(self, item) :
        try:
            self.tell(item) 
            return True
        except KeyError :
            return False
        except IndexError :
            return False            
            
# End class FileIndex   
    

def find_command(command, path=None):
    """Return the full path to the first match of the given command on
    the path.
    
    Arguments:
    - command -- is a the name of the executable to search for.
    - path -- is an optional alternate path list to search. The default it
        to use the COREBIOPATH environment variable, if it exists, else the 
        PATH environment variable.
        
    Raises:
    - EnvironmentError -- If no match is found for the command.
    
    By default the COREBIO or PATH environment variable is searched (as well
    as, on Windows, the AppPaths key in the registry), but a specific 'path'
    list to search may be specified as well.  
        
    Author: Adapted from code by Trent Mick (TrentM@ActiveState.com)
    See: http://trentm.com/projects/which/
    """
    import _which
    if path is None :
        path = os.environ.get("COREBIOPATH", "").split(os.pathsep)
        if path==['']: path = None   

    try :
        match =_which.whichgen(command, path).next()
    except StopIteration, _which.WhichError:
        raise EnvironmentError("Could not find '%s' on the path." % command)
    return match



class ArgumentError(ValueError) :
    """ A subclass of ValueError raised when a function receives an argument
    that has the right type but an inappropriate value, and the situation is not
    described by a more precise exception such as IndexError. The name of the   
    argument or component at fault and (optionally) the value are also stored.
    """
    
    def __init__(self, message, key, value=None) :
        """ Args:
        - message -- An error message.
        - key -- The name of the argument or component at fault.
        - value -- Optional value of the argument.
        """ 
        ValueError.__init__(self, message)
        self.key = key
        self.value = value
# end class ArgumentError


class frozendict(dict):
    """A frozendict is a dictionary that cannot be modified after being created
     -  but it is hashable and may serve as a member of a set or a key in a
    dictionary.
    # Author: Adapted from code by Oren Tirosh
    """
    # See: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/414283
    
    def _blocked_attribute(obj):
        raise AttributeError, "A frozendict cannot be modified."
    _blocked_attribute = property(_blocked_attribute)

    __delitem__ =   _blocked_attribute
    __setitem__ =   _blocked_attribute
    clear =         _blocked_attribute
    pop =           _blocked_attribute
    popitem =       _blocked_attribute
    setdefault =    _blocked_attribute
    update =        _blocked_attribute
    
    def __new__(cls, *args, **kw):
        new = dict.__new__(cls)
        dict.__init__(new, *args, **kw)
        return new

    def __init__(self, *args, **kw):
        pass
    
    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            # Hash keys, not items, since items can be mutable and unhasahble.
            h = self._cached_hash = hash(tuple(sorted(self.keys())))
            return h

    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)    
# end class frozendict   
          