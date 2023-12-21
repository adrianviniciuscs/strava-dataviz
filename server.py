from flask import Flask, render_template
from graphs import plotGraphs
from request import requestStravaAPI, checkAPIKeys
from createcsv import createCSV
app = Flask(__name__)


checkAPIKeys()
data = requestStravaAPI()
df = createCSV(data)

@app.route('/')
def index():
    scripts_and_divs = plotGraphs(df)
    return render_template('index.html', components=scripts_and_divs)


if __name__ == '__main__':
    app.run(debug=True)
