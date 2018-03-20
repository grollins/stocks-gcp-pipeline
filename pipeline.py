from os import environ
from datetime import datetime, timedelta


import google.auth
import pandas as pd
import quandl as qdl

import luigi
from luigi.contrib.gcs import GCSClient, GCSTarget


CREDENTIALS, _ = google.auth.default()
GCS_CLIENT = GCSClient(CREDENTIALS)
BUCKET_PATH = 'gs://senpai-io.appspot.com/test2'

TOKEN = environ['QUANDL_TOKEN']
qdl.ApiConfig.api_key = TOKEN


class GenerateQuandlReport(luigi.Task):
    date = luigi.DateParameter(default=datetime.today())

    def requires(self):
        return []

    def output(self):
        output_path_template = '{}/report/{date:%Y-%m-%d}.txt'
        output_path = output_path_template.format(BUCKET_PATH, date=self.date)
        return GCSTarget(output_path, client=GCS_CLIENT)

    def run(self):
        ticker_df = pd.read_csv('djia_symbols.csv')
        ticker_list = ticker_df.symbol.tolist()

        with self.output().open('w') as out_file:
            out_file.write(ticker_list)


if __name__ == '__main__':
    luigi.run()

