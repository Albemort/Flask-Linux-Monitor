from flask import Flask
from read import readfile
from monitor import Monitor

app = Flask(__name__)
data = readfile()
getdata = Monitor()

@app.route('/result', methods=['GET'])
def result():
    data.__init__()
    return data.measurements

@app.route('/result/refresh', methods=['POST'])
def refresh():
    getdata.get_statistics()
    return "OK", 200

if __name__ == '__main__':
    app.run(host='192.168.0.101', port=5000, debug=False)