from django.urls import path
from erp.views import *

# o redirecionamento pode ser feito por caminho absoluto (ex: '/erp/'),
# ou por nome (usando o 'name' da URL): usando reverse_lazy('app_name:name_do_path')

app_name='erp'

urlpatterns = [
    #path('', home),  # FBV do home...
    path('', HomeView.as_view(), name='home'),  # CBV precisa do as_view() !!!
    
    # Funcionários -------------------------------------------------------------------
    path('funcionarios/', listarFuncionarios, name='lista_funcionarios'),
    path('funcionarios/novo', criaFuncionario, name='cria_funcionario'),
    path('funcionarios/detalhe/<id>', buscaPorID, name='detalha_funcionario'), # se aqui eu pus "id", lá na view tem que ser "id" também
    path('funcionarios/atualiza/<id>', atualizaFuncionario, name='atualiza_funcionario'), # se aqui eu pus "id", lá na view tem que ser "id" também
    
    # Produtos -------------------------------------------------------------------
    path('produtos/', ListarProdutosView.as_view(), name='lista_produtos'),
    path('produtos/novo', ProdutoCreateView.as_view(), name='cria_produto'),
    path('produtos/atualiza/<pk>', AtualizarProdutoView.as_view(), name='atualiza_produto'), 
    # o UpdateView usa o parâmetro padrão 'pk' para comparar com as PKs do modelo no banco de dados
    path('produtos/detalhe/<pk>', DetalheProdutoView.as_view(), name='detalha_produto'),
    path('produtos/deleta/<pk>', DeletarProdutoView.as_view(), name='deleta_produto'),
    
    # Vendas -------------------------------------------------------------------
    path('vendas/', ListarVendasView.as_view(), name='lista_vendas'),
    path('vendas/novo', VendaCreateView.as_view(), name='cria_venda'),
    path('vendas/atualiza/<pk>', AtualizarVendaView.as_view(), name='atualiza_venda'),
    path('vendas/deleta/<pk>', DeletarVendaView.as_view(), name='deleta_venda'),
    path('vendas/detalhe/<pk>', DetalheVendaView.as_view(), name='detalha_venda'),
]