from flask import Flask, render_template

app = Flask(__name__)

@app.route('/bank-marketing/', methods=["GET", "POST"])
def bank_marketing():
    return render_template('bankMarketing.html', name="holanda")