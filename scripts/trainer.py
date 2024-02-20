import h2o
from h2o.automl import H2OAutoML

import pandas as pd


df = pd.read_csv('../data/rating.csv')


h2o.init()


h2o_df = h2o.H2OFrame(df)

x = h2o_df.columns[:-1] 
y = 'rating'

train, test = h2o_df.split_frame(ratios=[0.8], seed=42)


aml = H2OAutoML(max_runtime_secs=600)  


aml.train(x=x, y=y, training_frame=train)


model_path = h2o.save_model(aml.leader, path="../model", force=True)

h2o.shutdown()
