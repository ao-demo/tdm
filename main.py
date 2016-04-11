from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def hello():
    filename = '/tmp/result'
    ret_str = "Apporbit data anonymizer <br/>"
    if os.path.isfile(filename):
        with open(filename, 'r') as infile:
            str = infile.readline()
        if str == 'success':
            ret_str += "Data masking completed"
        elif str == 'failure':
            ret_str += "Data masking failed"
    else:
        ret_str += "Data masking in progress.."

    return ret_str


if __name__ == "__main__":
    app.run(host="0.0.0.0")
