import os
import filecmp


def compile_code(file):
    class_file = file[:-4]
    if os.path.isfile(class_file):
        os.remove(class_file)
    if os.path.isfile(file):
        os.system('g++ -std=c++11 -o '+class_file+' '+file)
        if os.path.isfile(class_file):
            return 200
        else:
            return 400
    else:
        return 404

def run_code(file, input_file, output_file, timeout, mem_limit):
    print(file)
    print(input_file)
    print(output_file)

    class_file = file[:-4]
    os.system('g++ -std=c++11 -o ' + class_file + ' ' + file)
    cmd = os.getcwd() + "/" + class_file
    r = os.system('timeout '+ timeout +' ' + cmd + ' < '+input_file+' > ' + output_file)
    print(r)

    if r == 0:
        return 200
    elif r == 31744:
        #os.remove(output_file)
        return 408
    else:
        #os.remove(output_file)
        return 400


def match(output_file, answer):
    if os.path.isfile(output_file) and os.path.isfile(answer):
        f1 = open(output_file, "r")
        f2 = open(answer, "r")
        b = f1.read() == f2.read()
        #b = filecmp.cmp(output_file, answer)
        #os.remove(output_file)
        return b
    else:
        return 404