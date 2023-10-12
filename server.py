from flask import Flask, render_template
from bokeh.embed import components
from graphs import grid

app = Flask(__name__)

@app.route('/')
def index():
    # Generate the script and div components for the grid
    script, div = components(grid)

    return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
    app.run(debug=True)

