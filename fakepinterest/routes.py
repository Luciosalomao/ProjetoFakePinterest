from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        user = Usuario.query.filter_by(email=formlogin.email.data).first()
        if user:
            bcrypt.check_password_hash(user.senha, formlogin.senha.data)
            login_user(user, remember=True)
            return redirect(url_for('perfil', id_usuario=user.id))
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        pwd = bcrypt.generate_password_hash(formcriarconta.senha.data)
        user = Usuario(usuario=formcriarconta.usuario.data,
                       nome=formcriarconta.nome.data,
                       email=formcriarconta.email.data,
                       senha=pwd)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('perfil', id_usuario=user.id))
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', user=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
    return render_template('perfil.html', user=usuario, form=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/feed')
@login_required
def feed():
    '''Limitando a quantidade de 100 imagens'''
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:100]
    return render_template('feed.html', fotos=fotos)