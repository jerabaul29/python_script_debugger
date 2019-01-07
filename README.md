# python_script_debugger

## Aim

The aim of this repository is to provide a bit of code to make debugging of Python scripts easier and faster. In particular, I found that I usually spend a lot of time fixing small problems in my Python scripts, such as indexes and slicing during plotting. Unfortunately, this becomes quickly time consuming in particular when the script itself has to do a bit of data processing and takes time.

So I wrote this code in order to let me easily get to an IPython prompt at the locations where some problems are encountered.

## Installation

You will need ipython:

```pip install ipython```

Then, simply clone this repo to get the code.

In addition, I like to call this using the following bashrc function:

```
p(){
    ipython PATH_TO_GIT_REPO/python_script_debugger/python_script_debugger/script_debugger.py -- $1
}
```

where PATH\_TO\_GIT\_REPO should lead to the python_script_debugger repo.

## Use

To use, simply call on the script. For example, I can do this kind of things on the *example/* scripts:

```
(VE_P2) ✔ jrlab-T150s:~/Desktop/Git/python_script_debugger/example [master|✚ 1]> p simple_bugged.py 
execute simple_bugged.py 


now comes a problem
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-1-6b4382d9b5cc> in <module>()
      3 #-3->
      4 #-4-> print("now comes a problem")
----> 5 b = a / 0.0
      6 #6->
      7 #7-> print(b)

ZeroDivisionError: float division by zero
 


start IPython from exception point:

In [1]: b
Out[1]: 0

In [2]: a
Out[2]: 4.5

In [3]: b = a / 2.0

In [4]: exit

resuming at next line



2.25
hit the end
```

This works also fine with, for example, matplotlib figures.
