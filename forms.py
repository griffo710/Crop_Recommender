from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class CropPredictionForm(FlaskForm):
    N = FloatField('Nitrogen (N)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 90", "type": "number", "step": "0.1"})
    P = FloatField('Phosphorus (P)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 42", "type": "number", "step": "0.1"})
    K = FloatField('Potassium (K)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 40", "type": "number", "step": "0.1"})
    temperature = FloatField('Temperature (°C)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 25", "type": "number", "step": "0.1"})
    humidity = FloatField('Humidity (%)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 60", "type": "number", "step": "0.1"})
    ph = FloatField('pH Level', validators=[InputRequired()], render_kw={"placeholder": "e.g. 6.5", "type": "number","step": "0.1"})
    rainfall = FloatField('Rainfall (mm)', validators=[InputRequired()], render_kw={"placeholder": "e.g. 100", "type": "number", "step": "0.1"})
    submit = SubmitField('Predict')

# Data required  treats 0 as invalid input. Therefor InputRequired is used instead of DataRequired.
