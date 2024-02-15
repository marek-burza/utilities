[own_path, ~, ~] = fileparts(mfilename('fullpath'));
module_path = fullfile(own_path, '..');
python_path = py.sys.path;
if count(python_path, module_path) == 0
    insert(python_path, int32(0), module_path);
end
py.our_module.our_script.our_function('Hello')
