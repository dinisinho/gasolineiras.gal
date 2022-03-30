#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, request, redirect, url_for
from functions import listaConcelhos, datosConcelho
from forms import formBusqueda, lista_concellos, t_ordepor
from wtforms.validators import DataRequired	

from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

@app.route('/', methods=["GET", "POST"])
def index():
    form = formBusqueda(request.form)
    if form.validate_on_submit():
        concello = form.concello.data
        ordepor = form.ordepor.data
    if 'concello' in locals():
        if not 'ordepor' in locals():
            ordepor = 'nada'            

        lista_gasolineiras = datosConcelho(concello, ordepor)
        for a in lista_concellos:
            if a[0] == concello:
                nome_concello = a[1]
        for a in t_ordepor:
            if ordepor == a[0]:
                d_ordepor = {'cod' : a[0], 'nome' : a[1]}
        return render_template('por_concelho.html', concello = nome_concello, gasolineiras = lista_gasolineiras, ordepor = d_ordepor, form=form)
    else:
        return render_template('por_concelho.html', form=form)

@app.route('/sobre/')
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    app.run(debug=True, host="192.168.0.45") #Só para debug en DEV
    #serve(app)