import pandas as pd
import joblib

class CropPredictor():
    """
    - This class is responsible for loading the trained crop recommendation model and
    making predictions based on input features.
    - It takes the input features, processes them into the required format, 
    and uses the model to predict the best crops along with their confidence scores. 
    - The predictions are returned as a list of tuples containing the crop name and its corresponding confidence score.
    - The model is loaded from a specified file path during the initialization of the class.
    - The predict method takes a dictionary of features, converts it into a DataFrame, and returns the 
    top 3 crop recommendations based on the predicted probabilities. 
    """
    def __init__(self, model):
        self.model = joblib.load(model)

    def predict(self, features):
        input_data = pd.DataFrame(features, index=[0])
        probabilities = self.model.predict_proba(input_data)[0]
        crops = self.model.classes_
        crop_probs = list(zip(crops, probabilities))
        crop_probs.sort(key=lambda x: x[1], reverse=True)
        top3 = crop_probs[:3]
        return top3