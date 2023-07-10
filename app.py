from flask import Flask, render_template, request
from extractive import summarizer
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        a, b, c, d = summarizer(rawtext)
    else:
        a, b, c, d = "dd", "dd", 0, 0  # Default values if no POST request is made

    return render_template('sumary.html', summ=b, orig=a, len_orig=c, len_summ=d)

port = int(os.environ.get('PORT', 5000))
debug = bool(os.environ.get('DEBUG', True))

if __name__ == '__main__':
    app.run(port=port, debug=debug)
