from flask import Flask, render_template
from twitter_trending import get_trending_topics

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script')
def run_script():
    result = get_trending_topics()
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
