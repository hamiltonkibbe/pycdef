#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Hamilton Kibbe <ham@hamiltonkib.be>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


def cdef(variable, var_name=None, precision='single', export_length=False,
         length_name=None, static=False, pack=True, line_length=80):
    """ Generate c language definition for a constant array.

    Paramters
    ---------
    variable : an iterable
        list or array for which to generate a definition

    var_name : string
        Name to use for the variable in the generated definition. If var_name
        is None, cdef will try to determine the name of the variable passed to
        it and use that. If it is unable to determine the variable name it will
        default to 'unnamed'

    precision : string
        Precision of the generated definition. May be 'single' (float) or
        'double' (double).

    export_length : bool
        If export_length is True, the definition will generate a variable
        holding the length of the array.

    length_name : string
        If export_length is True, this argument sets the name to use for the
        variable holding the length of the generated array. If length_name is
        None, cdef will default to using '<var_name>Length'

    static : bool
        If static is True, cdef will prefix the definition with a static access
        specifier.

    pack : bool
        If pack is True, the generated definition will put as many values on a
        line as possible. The maximum number of characters to put on a single
        line can be set using the `line_length` parameter. If `pack` is false,
        each value is put on its own line.

    line_length : int
        Maximum number of characters to print on a single line. This is only
        used if the `pack` paramter is set to True
    """

    if var_name is None:
        import inspect
        # Yeah, Yeah I know... But who doesn't like a little magic
        magic_varname = inspect.stack()[1][4][0].split('(')[1].split(',')[0].split(' ')[0].split(')')[0]
        var_name = magic_varname if not any(c in magic_varname for c in '[({') else 'unnamed'


    if static:
        prefix = 'static const'
    else:
        prefix = 'const'

    if precision == 'single':
        typestr = 'float'
        fmtstr = '%1.10gf'
        zlfmtstr = '%1.1ff'
    else:
        typestr = 'double'
        fmtstr = '%1.19g'
        zlfmtstr = '%1.1f'


    values = ''
    line = '    '
    for i, value in enumerate(variable):
        if not pack:
            if i != len(variable) - 1:
                if int(value) == value:
                    fmt = '    %s,\n' % zlfmtstr
                else:
                    fmt = '    %s,\n' % fmtstr
            else:
                if int(value) == value:
                    fmt = '    %s\n' % zlfmtstr
                else:
                    fmt = '    %s\n' % fmtstr
            values += (fmt % value)
        else:
            if i != len(variable) - 1:
                if int(value) == value:
                    fmt = '%s, ' % zlfmtstr
                else:
                    fmt = '%s, ' % fmtstr
            else:
                if int(value) == value:
                    fmt = '%s' % zlfmtstr
                else:
                    fmt = '%s' % fmtstr
            valstr = fmt % values
            if (len(valstr) + len(line)) <= line_length:
                line += valstr
            else:
                values = '%s%s\n' % (values, line)
                line = '    ' + valstr
    if pack:
        values = '%s%s\n' % (values ,line)

    if export_length:
        length_name = length_name if length_name is not None else var_name + 'Length'
        defstr = '%s unsigned %s = %d;\n\n' % (prefix, length_name, len(variable))
        defstr += '%s %s %s[%s] =\n{\n%s};\n\n' % (prefix, typestr, var_name, length_name, values)
    else:
        defstr = '%s %s %s[%d] = {\n%s};\n\n' % (prefix, typestr, var_name, len(variable), values)
    
    print(defstr)



