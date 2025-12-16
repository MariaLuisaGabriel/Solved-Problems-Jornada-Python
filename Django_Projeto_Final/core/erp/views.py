from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, Http404
from erp.forms import FuncionarioForm, ProdutoForm
from erp.models import Funcionario, Produto, Venda
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ErpLoginView(LoginView):
    template_name = 'erp/login.html'
    redirect_authenticated_user = True # se o usuário já estiver autenticado, redireciona direto para o success_url
    success_url = reverse_lazy('erp:dashboard')

class ErpLogoutView(LogoutView):
    template_name = 'erp/logout.html'

# FBV - home
# def home(request: HttpRequest):
#     # primeiro método que uma página faz quando abre é um GET
#     if request.method == 'GET':
#         return render(request, template_name='erp/index.html')

# CBV - home
class HomeView(TemplateView):
    template_name='erp/index.html'

class DashboardView(LoginRequiredMixin, TemplateView): # home da parte privada do sistema (após login)
    template_name='erp/dashboard.html'

# Funcionários -------------------------------------------------------------------
# tudo FBV

@login_required 
# exige que o usuário esteja logado para acessar essa view
# (se não tiver logado, redireciona para o login.html o app)
def criaFuncionario(request: HttpRequest):
    
    if request.method == 'GET': # abrir o formulário
        form = FuncionarioForm()
        
        return render(request, template_name='erp/funcionarios/novo.html', context={'form': form})
    
    elif request.method == 'POST':
        form = FuncionarioForm(request.POST) # passa todos os dados escritos pelo usuário no formulário
        
        if form.is_valid(): # valida os dados
            
            funcionario = Funcionario(
                **form.cleaned_data # atribui automaticamente os dados do formulário aos campos respectivos do modelo (operador de desempacotamento)
            )
            
            funcionario.save() # salva no banco de dados
            
            return HttpResponseRedirect(redirect_to='/') #volta para a raíz da aplicação

@login_required 
def listarFuncionarios(request: HttpRequest):
    
    if request.method == 'GET': # só tratamos GET pois não há dados a serem passados para listagem (é sem filtragem)
        funcionarios = Funcionario.objects.all() # resgata todos os funcionarios do banco de dados, nesse caso sem filtragem
        
        return render(request, template_name='erp/funcionarios/lista.html', context={'funcionarios': funcionarios})

@login_required 
def atualizaFuncionario(request: HttpRequest, id: int):
    
    if request.method == 'GET': # renderizar os dados do funcionário cadastrado em um formulario para edição
        funcionario = Funcionario.objects.get(id=id)
        # precisa deixar claro que é instance!!
        form = FuncionarioForm(instance=funcionario) # busca pela instancia de formulario que tenha os dados do funcionario passado
        
        return render(request, template_name='erp/funcionarios/atualiza.html', context={'form': form})
    
    elif request.method == 'POST': # atualizar os dados do funcionário cadastrado
        funcionario = Funcionario.objects.get(id=id)
        # precisa deixar claro que é instance!!
        form = FuncionarioForm(request.POST, instance=funcionario) # usa os dados submetidos do formulario para atualizar a instância de formulário que coincide com os dados do funcionário
        
        if form.is_valid():
            form.save() # salva no banco de dados a instância de formulário atualizada
            
            return HttpResponseRedirect(redirect_to=f'/funcionarios/detalhe/{id}') # redireciona para a página de detalhes do funcionário atualizado

def buscaPorID(request: HttpRequest, id: int):
    
    if request.method == 'GET': # só tratamos GET, pois é para busca de dados
        try:
            funcionario = Funcionario.objects.get(id=id) # resgata o funcionário do banco de dados que tem o ID correspondente com o passado na URL
        except Funcionario.DoesNotExist:
            funcionario = None
        
        return render(request, template_name='erp/funcionarios/detalhe.html', context={'funcionario': funcionario})

# Produtos -------------------------------------------------------------------
# tudo CBV

# pus o LoginRequiredMixin primeiro para ele ser executado antes do CreateView
# (exigir o login primeiro, acima de tudo)
class ProdutoCreateView(LoginRequiredMixin, CreateView): # View que cria um novo produto
    template_name = 'erp/produtos/novo.html'
    model = Produto # modelo que ele usa para inserir dados no banco de dados quando essa classe é usada
    # fields = '__all__' # todos os campos do modelo Produto serão exibidos no formulário, só usado se não tiver criado classe de formulário
    
    # Obs: no caso desse projeto foi criado um formulário para produtos para poder colocar as labels
    # em português, mas o python é capaz de criar um automaticamente com os nomes dos campos do modelo Produto.
    
    form_class = ProdutoForm
    
    success_url = reverse_lazy('erp:home') # para onde redirecionar após o formulário ser submetido com sucesso (POST válido)

class ListarProdutosView(LoginRequiredMixin, ListView): # View que lista todos os produtos
    model = Produto
    template_name = 'erp/produtos/lista.html'
    context_object_name = 'produtos' # nome da variável que será usada no template para listar os produtos

class AtualizarProdutoView(LoginRequiredMixin, UpdateView): # View que atualiza um produto existente
    model = Produto
    template_name = 'erp/produtos/atualiza.html'
    
    form_class = ProdutoForm # usa o mesmo formulário de criação de produto para atualizar
    # inclusive, como é uma view de atualização, o formulário já virá preenchido com os dados
    # atuais do produto a alterar !!
    
    success_url = reverse_lazy('erp:lista_produtos') # quando atualiza, redireciona para a listagem de produtos
    
    # tratar para caso um produto não seja encontrado: (substitui a exceção Http404)
    def get_object(self, queryset=None):
        try: # executa normal caso o produto seja encontrado
            return super().get_object(queryset)
        except Http404: # se o produto não for encontrado, retornará None em vez de lançar exceção
            return None

class DetalheProdutoView(LoginRequiredMixin, DetailView):
    template_name = 'erp/produtos/detalhe.html'
    model = Produto
    
    context_object_name = 'produto' # nome da variável que será usada no template para exibir os detalhes do produto
    
    # tratar para caso um produto não seja encontrado: (substitui a exceção Http404)
    def get_object(self, queryset=None):
        try: # executa normal caso o produto seja encontrado
            return super().get_object(queryset)
        except Http404: # se o produto não for encontrado, retornará None em vez de lançar exceção
            return None

class DeletarProdutoView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'erp/produtos/deleta.html'
    
    context_object_name = 'produto' # variável para que o cliente confirme o produto a ser deletado
    
    success_url = reverse_lazy('erp:lista_produtos')
    
    # tratar para caso um produto não seja encontrado: (substitui a exceção Http404)
    def get_object(self, queryset=None):
        try: # executa normal caso o produto seja encontrado
            return super().get_object(queryset)
        except Http404: # se o produto não for encontrado, retornará None em vez de lançar exceção
            return None

class VendaCreateView(LoginRequiredMixin, CreateView): # View que cria uma nova venda
    template_name = 'erp/vendas/novo.html'
    model = Venda 
    fields = ['funcionario','produto']
    
    success_url = reverse_lazy('erp:home') # para onde redirecionar após o formulário ser submetido com sucesso (POST válido)

class ListarVendasView(LoginRequiredMixin, ListView): # View que lista todos os produtos
    model = Venda
    template_name = 'erp/vendas/lista.html'
    context_object_name = 'vendas' # nome da variável que será usada no template para listar os produtos

class DetalheVendaView(LoginRequiredMixin, DetailView):
    template_name = 'erp/vendas/detalhe.html'
    model = Venda
    
    context_object_name = 'venda' # nome da variável que será usada no template para exibir os detalhes do produto
    
    # tratar para caso uma venda não seja encontrada: (substitui a exceção Http404)
    def get_object(self, queryset=None):
        try: # executa normal caso a venda seja encontrada
            return super().get_object(queryset)
        except Http404: # se a venda não for encontrada, retornará None em vez de lançar exceção
            return None

class AtualizarVendaView(LoginRequiredMixin, UpdateView): # View que atualiza uma venda existente
    model = Venda
    template_name = 'erp/vendas/atualiza.html'
    
    fields = ['funcionario','produto']
    
    success_url = reverse_lazy('erp:lista_vendas') # quando atualiza, redireciona para a listagem de vendas
    
    # tratar para caso uma venda não seja encontrada: (substitui a exceção Http404)
    def get_object(self, queryset=None):
        try: # executa normal caso a venda seja encontrada
            return super().get_object(queryset)
        except Http404: # se a venda não for encontrada, retornará None em vez de lançar exceção
            return None

class DeletarVendaView(LoginRequiredMixin, DeleteView):
    model = Venda
    template_name = 'erp/vendas/deleta.html'
    
    context_object_name = 'venda' # variável para que o cliente confirme a venda a ser deletada
    
    success_url = reverse_lazy('erp:lista_vendas')
    
    # tratar para caso uma venda não seja encontrada: (substitui a exceção Http404)
    def get_object(self, queryset=None):
        try: # executa normal caso a venda seja encontrada
            return super().get_object(queryset)
        except Http404: # se a venda não for encontrada, retornará None em vez de lançar exceção
            return None