import os
import platform
import time


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
    if platform.system() == 'Windows':
        start_time = time.time()
        r = os.system(cmd + ' < '+input_file+' > ' + output_file)
        elapsed_time = time.time() - start_time
        if elapsed_time > int(timeout):
            r = 31744
    else:
        r = os.system('timeout '+ timeout + 's ' + cmd + ' < '+input_file+' > ' + output_file)
    if r == 0:
        return 200
    elif r == 31744:
        os.remove(output_file)
        return 408
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