from flask_wtf import FlaskForm
from wtforms import Form, FloatField, IntegerField, SelectField,StringField, RadioField, DecimalField
from wtforms.validators import Required
from wtforms.widgets import Input

class bankPredictionForm(FlaskForm):
    age = IntegerField()
    job = SelectField(choices=['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])
    marital = SelectField(choices=["married","divorced","single","unknown"])
    education = SelectField(choices=[
        ("basic.4y","basic 4y"),
        ("basic.6y","basic 6y"),
        ("basic.9y","basic 9y"),
        ("high.school","high school"),
        ("illiterate", "illiterate"),
        ("professional.course","professional course"),
        ("university.degree","university degree"),
        ("unknown","unknown")])
    default = RadioField(choices=['no', 'unknown', 'yes'])
    housing = RadioField( widget=Input(input_type="radio"),choices=["no","yes", "unknow"])
    loan = RadioField(choices=['no', 'unknown', 'yes'])
    contact = RadioField(choices=['cellular', 'telephone'])
    month= SelectField(choices=['apr', 'aug', 'dec', 'jul', 'jun', 'mar', 'may', 'nov', 'oct', 'sep'])
    day_of_week = SelectField(choices=['fri', 'mon', 'thu', 'tue', 'wed'])
    duration = IntegerField()
    campaign = IntegerField()
    pdays = IntegerField()
    previous = IntegerField()
    poutcome = RadioField(choices=['failure', 'nonexistent', 'success'])
    emp_var_rate = DecimalField("emp.var.rate",id="emp.var.rate",_prefix="emp.var.rate", places=2, rounding=None, use_locale=False, number_format=None)
    cons_price_idx = FloatField("cons.price.idx",id="cons.price.idx", _name="cons.price.idx")
    cons_conf_idx = FloatField("cons.conf.idx", id="cons.conf.idx", _name="cons.conf.idx")
    euribor3m = FloatField()
    nr_employed = FloatField("nr.employed")

    
