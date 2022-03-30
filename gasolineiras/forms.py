from flask_wtf import FlaskForm
from wtforms import Form, SelectField,SubmitField
from functions import listaConcelhos
from wtforms.validators import DataRequired	

global lista_concellos
lista_concellos = listaConcelhos()

global t_ordepor

t_ordepor = [
    ('nada', 'Non ordenar'),
    ('p_gasoleo_a', 'Gasóleo A'),
    ('p_gasoleo_p', 'Gasóleo Premium'),
    ('p_gasoleo_b', 'Gasóleo B'),
    ('p_gasolina_95', 'Gaolina 95'),
    ('p_gasolina_98', 'Gasolina 98')
]

class formBusqueda(FlaskForm):
    concello = SelectField('Concello', choices=lista_concellos, default='', validators=[DataRequired("Escolle un concello")])
    ordepor = SelectField('Ordenar prezo por', choices=t_ordepor)
    submit = SubmitField('Buscar')
