# Easy Deploy Template - Python

This easy deploy template is designed to make it simple for you to go from code to a deployable image quickly. It is intended to be used across any OS that can run Python, relieving you of the need to worry about shell commands or PowerShell commands. To be able to run this template, you must have Python installed.

## Make Build System

This project utilizes the Make build system, which allows us to unify the way we build all of our applications, whether we are using Python or a different language. This Python template includes several targets in the Makefile:

- `clean`
- `init`
- `run_dev`
- `dockerimage`
- `up`
- `down`

## Scripts

The `scripts` folder contains all the Python scripts called by the Makefile targets. The `get_py.py` script is used to get the alias that Python3 is set to on the system and use that as the Python command for calling the other files. This means that all files should be written in Python3 format. However, the `get_py.py` file itself is currently written in Python2, so that if you are trying to run this on a system that only has Python2 available, the file will still run, but you will get an error about Python3 not being available.

### `init` target

The `init` target sets up the Python environment for us, allowing us to keep a clean host environment and install any packages we want without leaving anything behind.

### `clean` target

The `clean` target helps us keep track of cleaning the project by removing the environment and any Python cache files left behind from running.

### `run_dev` target

The `run_dev` target initializes the environment and then installs packages to that environment that are listed in the `requirements.txt` file at the root of the repository.

### `dockerimage` target

The `dockerimage` target allows us to build the appropriate Docker image after we have assured that the project runs properly using the `run_dev` target.

### `up` target

The `up` target allows us to run the Docker container on any post environment that we are on.

### `down` target

The `down` target does the same as the `up` target, but by bringing the Docker container down.

## Getting Started

1. Edit the `main.py` file and any other necessary files in your `src` directory.
2. Update the `IMAGE` and `VERSION` variables in the Makefile so that the rest of the variables in the Makefile work properly.

The `init` and `run_dev` targets clean and initialize the project. The `dockerimage` target does not initialize the project because we do not need to copy the environment over to the Docker image; a new environment will be created when the Docker image is started.

Examine the `Dockerfile` to see that we are only copying the `src` folder, the `init_venv.py` file, and the `requirements.txt` file over to the Docker container before running the `init_venv` script, then installing the requirements and running the `main.py` file. If you need to add any other folders or files to the Docker container, add them to the `Dockerfile` appropriately, given the setup that already exists there.

If you need to remove files that are not already being removed by the `clean` operation in the Makefile, add the directory of what you want to have deleted in the `relative_paths_to_remove` variable in `clean.py`. The paths should be relative to the location of the `clean.py` file.

The `.gitignore` file ensures that all Python cache files, the Python environment, any .env files, and all Vim swap files are left out of the repo upon upload.

## Usage

Here's an overview of how to use the Easy Deploy Template:

1. Make sure your Python code is in the `src` directory and update the `requirements.txt` file with any necessary dependencies.
2. Update the `IMAGE` and `VERSION` variables in the Makefile.
3. Run `make init` to set up the Python environment.
4. Run `make run_dev` to initialize the environment and install the required packages.
5. Test your application locally to ensure it works as expected.
6. Run `make dockerimage` to build the Docker image.
7. Run `make up` to run the Docker container on your chosen environment.
8. If needed, run `make down` to bring the Docker container down.
