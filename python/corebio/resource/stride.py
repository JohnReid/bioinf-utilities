
#  Copyright (c) 2003 Gavin E. Crooks
#  Copyright (c) 2005 David D. Ding <dding@berkeley.edu>
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
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
#  THE SOFTWARE.

"""STRIDE: Protein secondary structure assignment from atomic coordinates.

This module provides an interface to STRIDE, a c program used to recognize
secondary structural elements in proteins from their atomic coordinates.

"""

from corebio.seq import Seq, protein_alphabet, Alphabet
from corebio.resource.astral import to_one_letter_code

# alphabet for stride secondary structure
stride_alphabet = Alphabet("HGIEBC12345678@&T")

# Dictionary for conversion between names and alphabet
stride_alphabet_names  = ( 
    "H", "AlphaHelix",
    "G", "310Helix",
    "I", "PiHelix",
    "E", "Strand",
    "b", "Bridge",
    "B", "Bridge",
    "C", "Coil",
    "1", "TurnI",
    "2", "TurnI'",
    "3", "TurnII",
    "4", "TurnII'",
    "5", "TurnVIa",
    "6", "TurnVIb",
    "7", "TurnVIII",
    "8", "TurnIV",
    "@", "GammaClassic",
    "&", "GammaInv",
    "T", "Turn"
    )


class Stride(object) :
    def __init__(self, stride_file) :
        """ Read and parse a STRIDE output file.
        
        args:
            - stride_file   : An open file handle
        attributes :
            - pdbid     : The PDB id.
            - res       : A list of Res objects, one per PDB resiude
        """     
        res =[]
        f=stride_file
        self.pdbid = f.readline()[75:79]
        for l in f:
            if l[0:3] =="ASG":
                res.append(Res(l)) 
                
        self.res = res # A list of Res objects
        
        self._res_dict = None

    def total_area(self) :
        """ Return the solvent accessible area """
        area = 0
        for i in self.res :
            area += i.solvent_acc_area
        return area
    
    def primary(self):
        """ Return the protein primary sequence as a Seq object."""
        return Seq(''.join([r.primary_seq for r in self.res]), protein_alphabet)
        
    def secondary(self):
        """Return the secondary structure of the protien as a Seq object"""
        return Seq(''.join([r.secondary_str for r in self.res]), stride_alphabet)
        
        
    def get_res(self, chainid, resid) :
        """ Return the given resiude """
        if not self._res_dict :
            d = {}
            for r in self.res :
                d[ (r.chainid, r.resid)] = r
            self._res_dict =d
        
        return self._res_dict[(chainid, resid)]

    
    
class Res(object):
    """ Structural information of a single resiude. An ASG line from a stride
        output file.
        
        Attributes :
         - chainid 
         - resid   
         - primary_seq 
         - secondary_str 
         - solvent_acc_area 
         - phi 
         - psi
    """
         
    def __init__(self, res_line) :
        """ Eats a single 'ASG' line from a stride file, splits it up  
        into parts and return a Res object."""
            
        if (len(res_line)<70): 
            raise ValueError("Line not long enough")
        try: 
            self.chainid = res_line[9:10]
            # STRIDE converts blank chain ids into dashes. Undo.
            if self.chainid=="-" : self.chainid = " "
                
            # In rare cases STRIDE columns can be misaligned. Grab extra 
            # white space to compensate.
            self.resid = res_line[10:15].strip() 
            self.primary_seq = to_one_letter_code[res_line[5:8].capitalize()]
            self.secondary_str = res_line[24:25]
            self.solvent_acc_area = float(res_line[64:71]) 
            self.phi = float(res_line[42:49].strip())
            self.psi = float(res_line[52:59].strip())
        except FloatingPointError:
            raise FloatingPointError("Can't float phi, psi, or area")
        except KeyError:
            raise KeyError("Can't find three letter code in dictionary")
        except LookupError:
            raise LookupError("One of the values is out of index of res_line")
            
                
            











        
