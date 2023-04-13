import os
import shutil
from init_venv import venv_path

relative_paths_to_remove = [
    "../env",
    "./__pycache__"
]

this_file_path = os.path.abspath(os.path.dirname(__file__))
for rel_path in relative_paths_to_remove:
    abs_path = os.path.join(this_file_path, rel_path)
    abs_path = os.path.abspath(abs_path)
    if os.path.exists(abs_path):
        shutil.rmtree(abs_path)
