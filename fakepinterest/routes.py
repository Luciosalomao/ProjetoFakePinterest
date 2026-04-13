from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto

@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        user = Usuario.query.filter_by(email=formlogin.email.data).first()
        if user:
            bcrypt.check_password_hash(user.senha, formlogin.senha.data)
            login_user(user, remember=True)
            return redirect(url_for('perfil', usuario=user.usuario))
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
        return redirect(url_for('perfil', usuario=user.usuario))
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', user=usuario)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))