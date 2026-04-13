from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=3, max=20)])
    botao = SubmitField('Confirmacao')

class FormCriarConta(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nome = StringField('Nome', validators=[DataRequired(), Length(min=5, max=20)])
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=5, max=20)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=3, max=20)])
    confirmacao_senha = PasswordField('Confirmação Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmar = SubmitField('Criar Conta')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já está cadastrado, faça login para continuar')
