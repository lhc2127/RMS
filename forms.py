from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm): #want to give 2 search options: either by location (facility name/city) or by diagnosis (diagnosis and severity) 
    #search_by = SelectField(
        #label= "Search by", choices = [("Facility_Name_x", "Facility Name"), ("Facility_City", "City"), ("APR DRG Description", "Diagnosis"), ("APR Severity of illness Description", "Severity")]
    location = StringField("Search by Facility Name or City", [DataRequired()])
    
    diagnosis = StringField("Search by Diagnosis", validators=[DataRequired()])

    severity = SelectField(
        label = "Severity", choices = [("Minor", "Minor"), ("Major", "Major"),("Moderate","Moderate"), ("Extreme", "Extreme") ]
    )
    submit = SubmitField("Search")
    

