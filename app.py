from flask import Flask, render_template, url_for, request
from utxo import UTXO

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def getBalance():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        valid_email = True
        total_balance = -1
        utxo_acc = UTXO(request.form['email'])
        try:
            total_balance = utxo_acc.displayBalance()
        except:
            valid_email = False
        finally:
            return render_template('index.html', useremail=request.form['email'], total_balance=total_balance, valid_email=valid_email)

if __name__ == '__main__':
    app.run()