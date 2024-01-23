import sys
import os
import subprocess
from init_venv import venv_path, site_packages, pip_cmd, python_cmd

this_file_path = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(this_file_path, '..', 'requirements.txt')

subprocess.run([pip_cmd, 'install', '-r', requirements_path])

# Update the sys.path to include the virtual environment's site-packages
sys.path.insert(0, site_packages)

# Now you can import packages installed in the virtual environment
# import some_package

main_file = os.path.join(this_file_path, '..', 'src', 'main.py')

# Run your main script
subprocess.run([python_cmd, main_file])
