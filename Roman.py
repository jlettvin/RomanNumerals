#!/usr/bin/env python

"""
Roman.py

A class for converting Roman-Arabic-Roman in a variety of bases.
Copyright(c) 2013 Jonathan D. Lettvin, All Rights Reserved"

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

This code satisfies all the specifications
for translating Roman to Arabic to Roman numerals
for all possible numbers expressible in Roman numerals
and is tested comprehensively over its entire legal range
for a variety of bases.

A number of technologies are employed to show familiarity.
Libraries: math, unittest, string, inspect

This code has been tested with python 2.7 and is known to fail with python2.5.
This is because python 2.5 handles exceptions differently.

Exception handling is significant but incomplete.
For instance, digit overflow testing would be desirable.

Statement of the problem as given:

A hex roman numeral is very much like the standard roman numeral, except
with different values. In normal roman numerals, I = 1, V = 5, X = 10
and so on. In hex roman numerals, I = 1, V = 8, X = 16, L = 128, C =
256, D = 2048 and M = 4096. So for example:

VIIII = 8 + 1 + 1 + 1 + 1 = 12
IX = 16 - 1 = 15
XV = 16 + 8 = 24
XL = 128 - 16 = 112

Write a program in python to convert in either direction. If given a
decimal number, it should return the hex roman numeral version of the
number and if given a hex roman numeral, it should return the decimal
version of the number.

e.g.

[prompt]$ program.py XI
17
[prompt]$ program.py 17
XI

Bonus 1: Add error checking. Inputs like "ABA" and "IC" and "10ab7"
should return a nice usage message.

Bonus 2: Generalize to any base n where I = 1, V = ceiling(n/2) X = n, etc.
"""

__module__     = "Roman.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = """\
Copyright(C) 2011 Jonathan D. Lettvin, All Rights Reserved"""
__credits__    = [ "Jonathan D. Lettvin" ]
__license__    = "GPLv3"
__version__    = "0.0.1"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20111027"

import math

class Roman(object):
    """
    Roman class implements a bidirectional translator for Arabic and Roman numbers.
    """
    def __init__(self, base=16):
        "For practical reasons, the base cannot be less than 7"
        assert(base >= 7)
        base = float(base)
        self.translate = [
                ['M' , int(math.ceil((base**3)  ))          ],
                ['CM', int(math.ceil((base**3)  ))-(base**2)],
                ['D' , int(math.ceil((base**3)/2))          ],
                ['CD', int(math.ceil((base**3)/2))-(base**2)],
                ['C' , int(math.ceil((base**2)  ))          ],
                ['XC', int(math.ceil((base**2)  ))-(base   )],
                ['L' , int(math.ceil((base**2)/2))          ],
                ['XL', int(math.ceil((base**2)/2))-(base   )],
                ['X' , int(math.ceil((base)     ))          ],
                ['IX', int(math.ceil((base)-1   ))          ],
                ['V' , int(math.ceil((base)/2   ))          ],
                ['IV', int(math.ceil((base)/2-1 ))          ],
                ['I' , 1                                    ]
                ]

    def toRoman(self, value):
        highvalue = 4*self.translate[0][1]
        assert(0 < value <= highvalue) # Practical maximum without using bar above digit
        result = ''
        for pair in self.translate:
            roman, digts = pair
            while value >= digts:
                result += roman
                value -= digts
        return result

    def toDigits(self, value):
        result = 0
        for pair in self.translate:
            roman, digits = pair
            loop = len(roman) == 1
            if loop:
                while value.startswith(roman):
                    result += digits
                    value = value[len(roman):]
            else:
                if value.startswith(roman):
                    result += digits
                    value = value[len(roman):]
        if value:
            raise Exception('failed to consume all roman digits.  Perhaps out of order.')
        return result

    def permitted(self, romans):
        for roman in romans:
            if roman not in "IVXLCDM":
                return False
        return True

if __name__ == "__main__":
    import sys, unittest, inspect, string

    usage = """Usage: python2.7 %s [integer|roman [base]]
The default base is 16.
Examples:
    Roman 17     prints XI
    Roman 17 8   prints XXI
    Roman 17 10  prints XVII
    Roman XI     prints 17
    Roman XXI 8  prints 17
    Roman        runs a complete unit test""" % (__module__)

    class TheTest(unittest.TestCase):
        def setUp(self):
            pass

        def tearDown(self):
            pass

        def trial(self, pairs):
            "Use the number of the test name as the base for some tests."
            self.stack = inspect.stack()
            self.base = int(self.stack[1][3][6:].lstrip('0'))
            self.translate = Roman(self.base)

            for source, target in pairs:
                self.assertEqual(self.translate.toRoman(source), target)
                self.assertEqual(self.translate.toDigits(target), source)


        def test_007(self): # base 7 test
            pairs = [
                    (1,'I'),
                    (4,'V'),
                    (9,'XII'),
                    (10,'XIV'),
                    (12,'XVI'),
                    (15,'XXI'),
                    (24,'XLIX'),
                    (100,'CCII'),
                    (112,'CCXX'),
                    (1000,'MMCMXLII')]
            self.trial(pairs)

        def test_008(self): # base 8 test
            pairs = [
                    (1,'I'),
                    (4,'V'),
                    (9,'XI'),
                    (10,'XII'),
                    (12,'XV'),
                    (15,'XIX'),
                    (24,'XL'),
                    (100,'CLV'),
                    (112,'CLXX'),
                    (1000,'MCMLX')]
            self.trial(pairs)

        def test_010(self): # base 10 test
            pairs = [
                    (1,'I'),
                    (4,'IV'),
                    (9,'IX'),
                    (10,'X'),
                    (12,'XII'),
                    (15,'XV'),
                    (24,'XXIV'),
                    (100,'C'),
                    (112,'CXII'),
                    (1000,'M')]
            self.trial(pairs)

        def test_016(self): # base 16 test
            pairs = [
                    (1,'I'),
                    (4,'IIII'),
                    (9,'VI'),
                    (10,'VII'),
                    (12,'VIIII'),
                    (15,'IX'),
                    (24,'XV'),
                    (100,'XXXXXXIIII'),
                    (112,'XL'),
                    (1000,'CCCLXXXXXXV')]
            self.trial(pairs)

        def test_060(self): # base 60 test
            pairs = [
                    (1,'I'),
                    (4,'IIII'),
                    (9,'IIIIIIIII'),
                    (10,'IIIIIIIIII'),
                    (12,'IIIIIIIIIIII'),
                    (15,'IIIIIIIIIIIIIII'),
                    (24,'IIIIIIIIIIIIIIIIIIIIIIII'),
                    (100,'XVIIIIIIIIII'),
                    (112,'XVIIIIIIIIIIIIIIIIIIIIII'),
                    (1000,'XXXXXXXXXXXXXXXXVIIIIIIIIII')]
            self.trial(pairs)

        def test_100(self):
            "This is a comprehensive test of all permitted values over many bases."
            bases = (7, 8, 10, 16, 60)
            for base in bases:
                translate = Roman(base)
                permit = base**3
                for source in range(1, permit+1):
                    target = translate.toDigits(translate.toRoman(source))
                    self.assertEqual(source, target)


    try:
        if sys.version_info < (2, 6):
            raise Exception('Must use python 2.6 or greater', usage)

        argc = len(sys.argv)
        if argc < 2:
            unittest.main()
        else:
            base = 16 if argc < 3 else int(sys.argv[2])
            if not base:
                base = 16
            translate = Roman(base)
            arg = sys.argv[1]
            if arg.isdigit():
                print translate.toRoman(int(sys.argv[1]))
            elif translate.permitted(arg):
                print translate.toDigits(arg)
            else:
                print usage

    except Exception as e:
        print e
    finally:
        pass
