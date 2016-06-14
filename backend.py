import subprocess
import os
import platform
import website
import resource

def compile_code(file):
    class_file = file[:-4]
    if os.path.isfile(class_file):
        os.remove(class_file)
    if os.path.isfile(file):
        if platform.system() == 'Windows':
            os.system('g++ -g ' + file + ' -o ' + class_file + ' -lm')
            if os.path.isfile(class_file + '.exe'):
                return 200
            else:
                return 400
        else:
            os.system('g++ -std=c++11 -o '+class_file+' '+file)
            if os.path.isfile(class_file):
                return 200
            else:
                return 400
    else:
        return 404


def run_code(file, input_file, output_file, timeout, mem_limit):
    class_file = file[:-4]
    cmd = os.getcwd() + "/" + class_file

    command_line = ""
    if platform.system() == 'Windows':
        command_line = cmd + ' < '+input_file+' > ' + output_file
    else:
        command_line = 'ulimit -v ' + str(1000 * website.MEMORY_LIMIT) + ' && '+ \
                       cmd + ' < '+input_file+' > ' + output_file

    try:
        r = subprocess.check_call(
            command_line,
            stderr = subprocess.STDOUT,
            shell = True,
            timeout=float(website.TIME_LIMIT))

        memory = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if memory > 1000 * website.MEMORY_LIMIT and r == 0:
            r = 32512

    except subprocess.TimeoutExpired:
        r = 31744
    except subprocess.CalledProcessError as e:
        r = e.returncode

    if r == 0:
        return 200
    elif r == 31744:
        os.remove(output_file)
        return 408
    elif r == 32512:
        return 407
    else:
        os.remove(output_file)
        return 400


def match(output_file, answer):
    if os.path.isfile(output_file) and os.path.isfile(answer):
        f1 = open(output_file, "r")
        f2 = open(answer, "r")
        b = f1.read() == f2.read()
        f1.close()
        f2.close()
        os.remove(output_file)
        return b
    else:
        return 404