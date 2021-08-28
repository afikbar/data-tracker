# Data Tracker

Data Tracker is a Python web-service to track cryptocurrency quotes.

## Built With

* Python (3.9+)
* Flask
* [Cryptowatch REST API](https://docs.cryptowat.ch/rest-api/)

## Getting Started

1. Clone the repo
   ```sh
   git clone https://github.com/afikbar/data-tracker.git
   cd data-tracker
   ```
2. Install requirements.
    1. If using `conda`:
   ```sh
   conda env create -f environment.yml
   conda activate data-tracker
   ```
    2. If you prefer `pip`:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Flask server:
   ```sh
   python -m flask run
   ```
4. Visit `http://127.0.0.1:5000/`.

## Usage

1. Select your market of interest from the combo-box.
2. Select the pair you are interested in from the combo-box.
3. Click 'Go', and you'll be redirected to a new page showing metrics of your selection.

**_NOTE:_**  Not all markets have data for all the pairs, in this case, you'll get 'No data' message.

**_TIP:_** Variance rank is calculated within entire selected market, over the last 24 hours of available data. 

## License

[MIT](https://choosealicense.com/licenses/mit/)