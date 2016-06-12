from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/result/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['datafile']
        f.save(f.filename)
        # TODO run tests here and return result
        return 'file uploaded successfully'

if __name__ == "__main__":
    app.run()
