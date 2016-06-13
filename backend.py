import os
import filecmp


def compile_code(file):
    class_file = file[:-4]
    if os.path.isfile(class_file):
        os.remove(class_file)
    if os.path.isfile(file):
        os.system('gcc -o '+class_file+' '+file)
        if os.path.isfile(class_file):
            return 200
        else:
            return 400
    else:
        return 404


def run_code(file, input_file, output_file, timeout, mem_limit):
    cmd = './'+file
    r = os.system('timeout '+timeout+' '+cmd+' < '+input_file+' > ' + output_file)
    os.remove(file)
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
        b = filecmp.cmp(output_file, answer)
        os.remove(output_file)
        return b
    else:
        return 404

compile_code('bla.cpp')

