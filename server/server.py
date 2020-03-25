from flask import Flask, request

app = Flask(__name__)

@app.route('/hello', methods=['GET','POST'])
def return_msg():
    if request.method == "POST":
        return "server works"
    return "shit"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001)