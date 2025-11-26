from django import forms
from erp.models import Funcionario, Produto

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'sobrenome', 'cpf', 'email_funcional', 'remuneracao']

# Usar ModelForm evita ter que criar os campos manualmente, como abaixo, caso tivesse sido usado forms.Form:

    # nome = forms.CharField(label='Nome', max_length=30, required=True)
    # sobrenome = forms.CharField(label='Sobrenome', max_length=70, required=True)
    # cpf = forms.CharField(label='CPF', max_length=14, required=True)
    # email_funcional = forms.EmailField(label='Email Funcional', required=True)
    # remuneracao = forms.DecimalField(label='Remuneração', max_digits=8, decimal_places=2, required=True)

# Formulário criado só para alterar as Labels

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'preco': 'Preço',
        }