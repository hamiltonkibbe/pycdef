#pycdef

Generate C/C++ constant definitions from python variables.

## Printing to console
By default, pycdef will print the definition to the console.
Example:

```python
import numpy as np
from pycdef import cdef

TestVector = np.hamming(10)
cdef(TestVector)
cdef(TestVector, precision='double')
cdef(TestVector, pack=False)
cdef(TestVector, var_name='HammingTestVector', static=False)
```

Generates the following:

```c
static const float TestVector[10] =
{
    0.07999999821f, 0.187619552f, 0.4601218402f, 0.7699999809f, 0.9722586274f, 
    0.9722586274f, 0.7699999809f, 0.4601218402f, 0.187619552f, 0.07999999821f
};

static const double TestVector[10] =
{
    0.080000000000000016, 0.18761955616527015, 0.46012183827321207, 
    0.76999999999999991, 0.97225860556151789, 0.97225860556151789, 
    0.76999999999999991, 0.46012183827321207, 0.18761955616527015, 
    0.080000000000000016
};

static const float TestVector[10] =
{
    0.07999999821f,
    0.187619552f,
    0.4601218402f,
    0.7699999809f,
    0.9722586274f,
    0.9722586274f,
    0.7699999809f,
    0.4601218402f,
    0.187619552f,
    0.07999999821f
};

const float HammingTestVector[10] =
{
    0.07999999821f, 0.187619552f, 0.4601218402f, 0.7699999809f, 0.9722586274f, 
    0.9722586274f, 0.7699999809f, 0.4601218402f, 0.187619552f, 0.07999999821f
};
```
