from django.db import models

# Create your models here.

class Funcionario(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    sobrenome = models.CharField(max_length=70, null=False, blank=False)
    cpf = models.CharField(max_length=14, null=False, blank=False)
    remuneracao = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    email_funcional = models.EmailField(null=False, blank=False)
    
    def __str__(self): # deixar a representação em string do objeto mais bonitinha
        return f"{self.nome} {self.sobrenome} (ID: {self.id} - CPF: {self.cpf})"

class Produto(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(max_length=155, null=False, blank=False)
    preco = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    
    def __str__(self): # deixar a representação em string do objeto mais bonitinha
        return f"{self.nome} - R${self.preco} (ID: {self.id})"

class Venda(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)