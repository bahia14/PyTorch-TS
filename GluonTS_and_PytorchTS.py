'''


GluonTS and PytorchTS


https://analyticsindiamag.com/gluonts-pytorchts-for-time-series-forecasting/

https://github.com/mmaithani/data-science/blob/main/PyTorch_ts_time_series_forecasting(gluonts).ipynb

'''

#pip install pytorchts

#import pytorchts as pts
import matplotlib.pyplot as plt
import pandas as pd
import torch

from pts.dataset import ListDataset
from pts.model.deepar import DeepAREstimator
from pts import Trainer
from pts.dataset import to_pandas

url = "https://raw.githubusercontent.com/numenta/NAB/master/data/realTweets/Twitter_volume_AMZN.csv"
df = pd.read_csv(url, header=0, index_col=0, parse_dates=True)
df.head()

df[:100].plot(linewidth=2)
plt.grid(which='both')
plt.show()

import time
from datetime import datetime
FMT = '%H:%M:%S'


# training_data
training_data = ListDataset(
    [{"start": df.index[0], "target": df.value[:"2015-04-05 00:00:00"]}],
    freq = "5min"
)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

estimator = DeepAREstimator(freq="5min",
                            prediction_length=12,
                            input_size=43,
                            trainer=Trainer(epochs=15,
                                            device=device))
t1 = time.strftime(FMT, time.localtime())

predictor = estimator.train(training_data=training_data)

# calulando o tempo gasto
t2 = time.strftime(FMT, time.localtime())
tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
print("tempo de processamento: ", tdelta)

# test_data
test_data = ListDataset(
    [{"start": df.index[0], "target": df.value[:"2015-04-15 00:00:00"]}],
    freq = "5min"
)


for test_entry, forecast in zip(test_data, predictor.predict(test_data)):
    to_pandas(test_entry)[-60:].plot(linewidth=2)
    forecast.plot(color='b', prediction_intervals=[50.0, 90.0])
plt.grid(which='both')

