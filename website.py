from flask import Flask
from flask import render_template
from flask import request
import backend
import os
import sys
import platform

app = Flask(__name__)

INPUT_SUFFIX = ""
OUTPUT_SUFFIX = ".a"
TIME_LIMIT = "2" #seconds
MEMORY_LIMIT = 256 #MBs
INPUT_FILE_NAME = "aligator.in"
OUTPUT_FILE_NAME = "aligator.out"


@app.route("/")
def main():
    return render_template('index.html')


def is_suffix(test, suffix):
    if suffix == "":
        if "." in test:
            return False
        else:
            return True
    return test.endswith(suffix)


def check_test(test, filename):

    run_result = backend.run_code(filename, test[0], os.getcwd() + "/" + OUTPUT_FILE_NAME)
    if run_result == 408:
        return "TIME LIMIT EXCEEDED"
    if run_result == 407:
        return "MEMORY LIMIT EXCEEDED"
    if run_result == 400:
        return "RUNTIME ERROR"

    match_result = backend.match(os.getcwd() + "/" + OUTPUT_FILE_NAME, test[1])
    if match_result is False:
        return "WRONG ANSWER"
    return "OK"


@app.route('/result/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        runpath = os.path.dirname(os.path.realpath(sys.argv[0]))
        os.chdir(runpath)    # set current directory to the corrent value

        f = request.files['datafile']
        f.save(os.getcwd() + "/" + f.filename)

        compile_result = backend.compile_code(f.filename)
        if compile_result != 200:
            os.remove(f.filename)
            try:
                os.remove(OUTPUT_FILE_NAME)
            except:
                pass
            return "COMPILATION_ERROR"

        FULL_PATH = os.getcwd() + "/tests/"

        tests = os.listdir(FULL_PATH)
        tests.sort()

        test_pairs = list()
        timer = 0

        for test in tests:
            if not (is_suffix(test, INPUT_SUFFIX) or is_suffix(test, OUTPUT_SUFFIX)):
                continue
            if timer % 2 == 0:
                test_pairs.append(["", ""])
            test_pairs[len(test_pairs) - 1][timer % 2] = test
            timer += 1

        for i in range(len(test_pairs)):
            if is_suffix(test_pairs[i][0], OUTPUT_SUFFIX):
                tmp = test_pairs[i][0]
                test_pairs[i][0] = test_pairs[i][1]
                test_pairs[i][1] = tmp

            test_pairs[i] = [FULL_PATH + test_pairs[i][0], FULL_PATH + test_pairs[i][1]]

        id = 0
        for test in test_pairs:
            id += 1
            test_result = check_test(test, f.filename)
            if test_result != "OK":
                try:
                    os.remove(f.filename)
                    if platform.system() == 'Windows':
                        os.remove(f.filename[:-4] + '.exe')
                    else:
                        os.remove(f.filename[:-4])
                    os.remove(OUTPUT_FILE_NAME)
                except:
                    pass
                return test_result
        try:
            os.remove(f.filename)
            if platform.system() == 'Windows':
                os.remove(f.filename[:-4] + '.exe')
            else:
                os.remove(f.filename[:-4])
            os.remove(OUTPUT_FILE_NAME)
        except:
            pass
        return "OK"

if __name__ == "__main__":
    app.run()
