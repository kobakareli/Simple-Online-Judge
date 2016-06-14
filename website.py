from flask import Flask
from flask import render_template
from flask import request
import backend
import os
import platform

app = Flask(__name__)

INPUT_SUFFIX = "in"
OUTPUT_SUFFIX = "out"
TIME_LIMIT = "5"
MEMORY_LIMIT = 100 #MB
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
    open(OUTPUT_FILE_NAME, "w")

    run_result = backend.run_code(filename, test[0], os.getcwd() + "/" + OUTPUT_FILE_NAME, TIME_LIMIT, MEMORY_LIMIT)
    if run_result == 408:
        return "TIME LIMIT EXCEEDED"
    if run_result == 407:
        return "MEMORY LIMIT EXCEEDED"
    if run_result == 400:
        return "RUNTIME ERROR"

    match_result = backend.match(os.getcwd() + "/" + OUTPUT_FILE_NAME, test[1])
    if match_result == False:
        return "WRONG ANSWER"

    return "OK"

@app.route('/result/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['datafile']
        f.save(os.getcwd() + "/" + f.filename)

        compile_result = backend.compile_code(f.filename)
        if compile_result != 200:
            return "COMPILATION_ERROR"

        if platform.system() == 'Windows':
            FULL_PATH = os.getcwd() + "/tests/"
        else:
            FULL_PATH = os.getcwd() + "/PycharmProjects/Simple-Online-Judge/tests/"

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

            test_pairs[i]=[FULL_PATH + test_pairs[i][0] , FULL_PATH + test_pairs[i][1]]

        print(test_pairs)

        id = 0
        for test in test_pairs:
            id += 1
            print(id)
            test_result = check_test(test, f.filename)
            if test_result != "OK":
                return test_result

        return "OK"

if __name__ == "__main__":
    app.run()
