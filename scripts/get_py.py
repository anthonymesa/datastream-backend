import sys
import subprocess
import errno

def find_python3_command():
    major, minor = sys.version_info[:2]
    if major == 3:
        return sys.executable
    else:
        try:
            # Check if 'python3' command is available
            subprocess.check_output(["python3", "--version"], stderr=subprocess.STDOUT)
            return "python3"
        except subprocess.CalledProcessError:
            pass
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        # Check if 'python' command is actually Python 3
        try:
            output = subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)
            version = output.strip().split()[1]
            major, minor = map(int, version.split('.')[:2])
            if major == 3:
                return "python"
        except subprocess.CalledProcessError:
            pass
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    return None

python3_command = find_python3_command()

if python3_command:
    print("'{}'".format(python3_command))
else:
    print("null")

