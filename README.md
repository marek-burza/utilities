# Calling Python from Matlab

## Introduction

This source code explains how to call a function from a Python module from a Matlab script.

It is assumed that MATLAB and Python are already installed (along with NumPy in this particular example).

Exploring the topic I landed on [this link](https://mathworks.com/help/matlab/release-notes.html?startrelease=R2014b&endrelease=R2014b&searchHighlight=python) (MATLAB 2014b Release Notes) on the MathWorks website which indicated that it is possible starting from Matlab R2014b.


## Instructions

Start with a simple script [`our_script.py`](our_module/our_script.py):

    import numpy

    def our_function(text):
        print('%s %f' % (text, numpy.nan))

It has one function which prints the string passed to it as a parameter, followed by _NaN_ (not-a-number) value.

Keep it in its own directory [`our_module`](our_module).

Next, go to Matlab and navigate to the directory where the Python module (`our_module`). In your case this will be the directory where you cloned this repository to.

Call the function from the Python module with the following statement:

    py.our_module.our_script.our_function('Hello')

This will have the expected outcome:

    >> py.our_module.our_script.our_function('Hello')
    Hello nan
    >>

However, a [`matlab_script.m`](matlab_scripts/matlab_script.m) file in a [`matlab_scripts`](matlab_scripts) directory (created next to the `our_module` directory) with only the above statement will result in the following outcome:

    >> matlab_script
    Undefined variable "py" or class "py.our_module.our_script.our_function".

    Error in matlab_script (line 1)
    py.our_module.our_script.our_function('Hello')

    >>

Looking for the solution I found a [page](https://mathworks.com/help/matlab/matlab_external/undefined-variable-py-or-function-py-command.html) entitled _Undefined variable "py" or function "py.command"_ which helped to troubleshoot this error.

Assuming there is no typo in the script it recommends adding the base directory to Python's search path.

Therefore, the correct content of the Matlab script should be:

    [own_path, ~, ~] = fileparts(mfilename('fullpath'));
    module_path = fullfile(own_path, '..');
    python_path = py.sys.path;
    if count(python_path, module_path) == 0
        insert(python_path, int32(0), module_path);
    end
    py.our_module.our_script.our_function('Hello')

It obtains the location of the Python module, finds the base path of that module, accesses the Python search path, checks if the base path is already included and inserts it otherwise.

Running the corrected script will result in the same expected output as before.

[Here](https://mathworks.com/help/matlab/call-python-libraries.html) is another helpful link to het you going.
