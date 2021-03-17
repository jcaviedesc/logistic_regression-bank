from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/bank-marketing/')
def bank_marketing():
    return render_template('bankMarketing.html', name="holanda")