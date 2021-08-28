import re
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
import requests

_ALL_PRICES_URL = 'https://api.cryptowat.ch/markets/prices'
_KEYS_PATTERN = re.compile(r"(?P<type>index|market):(?P<market>.*):(?P<pair>.*)")

_DUMP_PATH = Path('data_tracker/data/24h_store')
_PLOTS_PATH = Path('static/plots')


class DataTracker:
    def __init__(self, all_prices_url: str = _ALL_PRICES_URL,
                 keys_pattern: re.Pattern = _KEYS_PATTERN,
                 dump_path: Path = _DUMP_PATH,
                 plot_path: Path = _PLOTS_PATH):
        self.all_prices_url = all_prices_url
        self.keys_pattern = keys_pattern
        self.dump_path = dump_path
        self.plots_path = plot_path

        self.dump_path.mkdir(exist_ok=True, parents=True)
        self.plots_path.mkdir(exist_ok=True, parents=True)

        self.available_markets = set()
        self.available_pairs = set()

        self._preload_existing_store()

    def _preload_existing_store(self):
        df = pd.read_parquet(self.dump_path, columns=['market', 'pair'])

        self.available_markets.update(df['market'].unique())
        self.available_pairs.update(df['pair'].unique())

    def get_all_current_prices(self):
        res = requests.get(self.all_prices_url)

        assert res.ok, f"Failed to fetch data. Status code: {res.status_code}."

        raw_data = res.json()['result']

        transformed_data = ({**self.keys_pattern.search(key).groupdict(), 'price': val}
                            for key, val in raw_data.items())

        df = pd.DataFrame.from_records(transformed_data)

        return df

    def persist(self):
        now = datetime.now().replace(second=0, microsecond=0)
        print(f"Persisting data for {now}...")
        now_df = self.get_all_current_prices()
        now_df.insert(0, 'timestamp', value=now)
        minutes_of_day = now.hour * 60 + now.minute

        self.available_markets.update(now_df['market'].unique())
        self.available_pairs.update(now_df['pair'].unique())

        now_df.to_parquet(self.dump_path / f"{minutes_of_day}.parquet", index=False)

    def view_data(self, market: str, pair: str):
        dump_df = pd.read_parquet(self.dump_path)
        market_df = dump_df.loc[(dump_df.market == market.lower())]
        pair_df = market_df.loc[market_df.pair == pair.lower(), ['timestamp', 'price']]

        if pair_df.empty:
            return f"No data available for {market.upper()}:{pair.upper()}."

        var_df = market_df.groupby('pair').agg({'price': 'var'})
        ranks = var_df.price.rank(pct=True, method='first', ascending=False)

        pair_rank = round(ranks[pair.lower()], 3)

        path = self.plots_path / market
        path.mkdir(exist_ok=True)

        pair_repr = f"{market.upper()}:{pair.upper()}"
        title = f"Last 24 Hours of '{pair_repr}'\nVariance rank among '{market.upper()}' is {pair_rank}"
        ax = pair_df.plot(x='timestamp', y='price', title=title, xlabel='Time',
                          ylabel='Price', legend=False, color='green')
        fig = ax.get_figure()
        img_path = path / f"{pair.lower()}.png"
        fig.savefig(img_path)
        return f"<img src='/{img_path.as_posix()}'/>"
