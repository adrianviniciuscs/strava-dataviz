from flask import Flask, render_template
from bokeh.embed import components
from graphs import plotGraphs
from request import requestStravaAPI, checkAPIKeys
app = Flask(__name__)


checkAPIKeys()
data = requestStravaAPI()

@app.route('/')
def index():
    scripts_and_divs = plotGraphs(data)
    return render_template('index.html', components=scripts_and_divs) 

if __name__ == '__main__':
    app.run(debug=True)
