import importlib
import importlib.util as importlib_util

def module_installed(module_name: str = None):
    assert module_name, ValueError("Missing a module name to check environment for.")
    assert isinstance(module_name, str), TypeError(f"module_name should be a string. Got type: ({type(module_name)})")
    
    return importlib_util.find_spec(module_name) is not None

def raise_import_err(module_name: str, module_path: str, missing_depends: list[str]):
    raise ImportError(f"Unable to import module '{module_name}' from {module_path}. Install the following package(s) to allow importing: {missing_depends}")