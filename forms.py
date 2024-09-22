from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField, RadioField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    category = SelectField('Which category would you like??',
                           choices=[('Spring', 'Spring'),
                                    ('Summer', 'Summer'),
                                    ('Autumn', 'Autumn'),
                                    ('Halloween', 'Halloween'),
                                    ('Winter', 'Winter'),
                                    ('Christmas', 'Christmas'),
                                    ('Christmas rom-com', 'Christmas rom-com')],
                           validators=[DataRequired()],
                           default='Spring')
    submit = SubmitField('Choose my film')


class AddForm(FlaskForm):
    title = StringField('Search for a film by entering its title below:', validators=[DataRequired()])
    submit = SubmitField('Search for Film')


class DetailsForm(FlaskForm):
    category = RadioField('Which of the below categories does this film belong to?',
                           choices=[('Spring', 'Spring'),
                                    ('Summer', 'Summer'),
                                    ('Autumn', 'Autumn'),
                                    ('Halloween', 'Halloween'),
                                    ('Winter', 'Winter'),
                                    ('Christmas', 'Christmas'),
                                    ('Christmas rom-com', 'Christmas rom-com')],
                           validators=[DataRequired()],
                           default='Spring')
    submit = SubmitField('Save film details')
