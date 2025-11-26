from django.contrib import admin
from erp.models import Funcionario, Produto, Venda

# Register your models here.
# Modelos específicos para o painel administrativo podem ser criados aqui

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'cpf', 'email_funcional', 'remuneracao')
    search_fields = ('nome', 'sobrenome', 'cpf', 'email_funcional')
    list_filter = ('remuneracao',)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco')
    search_fields = ('nome',)
    list_filter = ('preco',)

class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'funcionario', 'produto', 'data_venda')
    search_fields = ('funcionario__nome', 'produto__nome')
    list_filter = ('data_venda',)

admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Venda, VendaAdmin)