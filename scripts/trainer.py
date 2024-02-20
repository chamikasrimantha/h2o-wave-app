import h2o
from h2o.automl import H2OAutoML

import pandas as pd

# Load dataset
df = pd.read_csv('../data/rating.csv')


# Start H2O cluster
h2o.init()


# Convert DataFrame to H2O Frame
h2o_df = h2o.H2OFrame(df)

# Predictors and response
x = h2o_df.columns[:-1] 
y = 'rating'

# Split the data into train and test sets
train, test = h2o_df.split_frame(ratios=[0.8], seed=42)

# Initialize AutoML
aml = H2OAutoML(max_runtime_secs=600)  # Set the maximum runtime in seconds

# Train AutoML
aml.train(x=x, y=y, training_frame=train)

# Save the AutoML model
model_path = h2o.save_model(aml.leader, path="../model", force=True)


# Shutdown H2O cluster
h2o.shutdown()
