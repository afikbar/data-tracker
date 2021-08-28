from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, url_for, redirect
from data_tracker import DataTracker

tracker = DataTracker()

scheduler = BackgroundScheduler()
job = scheduler.add_job(tracker.persist, 'interval', minutes=1)
scheduler.start()

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html',
                           markets=sorted(map(str.upper, tracker.available_markets)),
                           pairs=sorted(map(str.upper, tracker.available_pairs)))


@app.route('/data-tracker/<pair>')
@app.route('/data-tracker/<market>/<pair>')
def view_data(pair: str, market: str = 'kraken'):
    return tracker.view_data(market, pair)


@app.route("/get_url_for_data", methods=["POST"])
def get_url_for_data():
    market = request.form['market']
    pair = request.form['pair']

    return redirect(url_for('view_data', market=market, pair=pair))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
