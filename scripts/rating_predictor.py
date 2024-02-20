import h2o
from h2o.automl import H2OAutoML
import pandas as pd

# Start H2O cluster
h2o.init()

# Load the saved AutoML model
model_path = "../model/model"  
loaded_model = h2o.load_model(model_path)

# Function to predict rating for a given actor and year
def predict_rating(actor, year):
    data = h2o.H2OFrame({'name': [actor], 'year': [year]})
    prediction = loaded_model.predict(data).as_data_frame()
    return prediction['predict'][0]


# Function to save predicted rating as result.csv for year xxxx
def caller():
    actor_names = ['vijay', 'Ajith', 'Surya', 'Rajini', 'Kamal Hasan']
    prediction_year = 2024
    data = []

    for name in actor_names:
        rating = predict_rating(name, prediction_year)
        data.append([name, rating])

    # Create a DataFrame from the list
    result_df = pd.DataFrame(data, columns=['Name', 'Rating'])

    # Save the DataFrame to a CSV file
    result_df.to_csv('../data/result.csv', index=False)

# call
caller()


# Shutdown H2O cluster
h2o.cluster().shutdown()
