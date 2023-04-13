import sys
import os
import venv

this_file_path = os.path.abspath(os.path.dirname(__file__))
venv_path = os.path.join(this_file_path, '..', "env")

# Determine the right paths and commands based on the platform
if sys.platform == "win32":
    site_packages = os.path.join(venv_path, "Lib", "site-packages")
    pip_cmd = os.path.join(venv_path, "Scripts", "pip")
    python_cmd = os.path.join(venv_path, "Scripts", "python")
else:
    site_packages = os.path.join(venv_path, "lib", "python{0}.{1}".format(*sys.version_info[:2]), "site-packages")
    pip_cmd = os.path.join(venv_path, "bin", "pip")
    python_cmd = os.path.join(venv_path, "bin", "python")

# Create a virtual environment if it doesn't exist
if not os.path.exists(venv_path):
    venv.create(venv_path, with_pip=True)
