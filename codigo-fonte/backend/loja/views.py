from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from decimal import Decimal
from .models import Produto, Pedido, ItemPedido, Cliente
from .forms import ProdutoForm, CEPForm

# --- Páginas Públicas ---
def home(request):
    return render(request, 'index.html')

def catalogo(request):
    produtos = Produto.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'catalogo.html', {'produtos': produtos})

# --- Autenticação de Cliente ---
def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(usuario=user, endereco="Não informado")
            login(request, user)
            return redirect('catalogo')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


# --- Lógica do Carrinho e Frete ---
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    subtotal_pedido = Decimal('0.0')
    form = CEPForm()
    
    # Recupera o frete da sessão, converte para Decimal
    valor_frete = Decimal(str(request.session.get('valor_frete', 0.0)))

    # Cálculo do frete via CEP
    if request.method == 'POST':
        form = CEPForm(request.POST)
        if form.is_valid():
            cep_destino = form.cleaned_data['cep']
            cep_origem = '32450000'  # CEP da loja
            peso_kg = '0.5'
            comprimento, altura, largura = 20, 10, 15

            # Aqui você deve chamar a API real de frete ou seu mock
            # Exemplo: substitua pelo código de cálculo correto
            try:
                # MOCK do frete: R$ 15,50
                valor_frete = Decimal('15.50')
                # Armazena na sessão como float
                request.session['valor_frete'] = float(valor_frete)
            except Exception as e:
                print(f"Erro ao calcular frete: {e}")
                messages.error(request, "Não foi possível calcular o frete. Verifique o CEP.")
                valor_frete = Decimal('0.0')
                request.session['valor_frete'] = 0.0

    # Itens do carrinho
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id))
        subtotal = produto.preco * quantidade
        itens_carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        subtotal_pedido += subtotal

    # Se o carrinho estiver vazio, zera o frete
    if not itens_carrinho:
        valor_frete = Decimal('0.0')
        request.session['valor_frete'] = 0.0

    total_geral = subtotal_pedido + valor_frete

    contexto = {
        'itens_carrinho': itens_carrinho,
        'subtotal_pedido': subtotal_pedido,
        'valor_frete': valor_frete,
        'total_geral': total_geral,
        'cep_form': form,
    }
    return render(request, 'carrinho.html', contexto)


def adicionar_ao_carrinho(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    carrinho = request.session.get('carrinho', {})
    produto_id = str(pk)
    quantidade = carrinho.get(produto_id, 0) + 1
    if quantidade <= produto.quantidade_estoque:
        carrinho[produto_id] = quantidade
        request.session['carrinho'] = carrinho
    return redirect('ver_carrinho')


def remover_do_carrinho(request, pk):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(pk)
    if produto_id in carrinho:
        del carrinho[produto_id]
        request.session['carrinho'] = carrinho
    return redirect('ver_carrinho')


def finalizar_pedido(request):
    if not request.user.is_authenticated:
        return redirect('login')

    carrinho = request.session.get('carrinho', {})
    valor_frete = Decimal(str(request.session.get('valor_frete', 0.0)))

    if not carrinho:
        return redirect('catalogo')

    try:
        with transaction.atomic():
            cliente = Cliente.objects.get(usuario=request.user)
            subtotal_pedido = Decimal('0.0')
            for produto_id, quantidade in carrinho.items():
                produto = get_object_or_404(Produto, id=int(produto_id))
                subtotal_pedido += produto.preco * quantidade
            
            total_geral = subtotal_pedido + valor_frete

            pedido = Pedido.objects.create(
                cliente=cliente,
                total=total_geral,
                valor_frete=valor_frete,
                status='em andamento'
            )

            for produto_id, quantidade in carrinho.items():
                produto = Produto.objects.get(id=int(produto_id))
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=quantidade,
                    subtotal=produto.preco * quantidade
                )
                produto.quantidade_estoque -= quantidade
                produto.save()

            del request.session['carrinho']
            del request.session['valor_frete']
            return render(request, 'pedido_confirmado.html', {'pedido': pedido})

    except Cliente.DoesNotExist:
        messages.error(request, "Perfil de cliente não encontrado.")
        return redirect('catalogo')
    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return redirect('ver_carrinho')


# --- CRUD de Produtos ---
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'admin/lista_produtos.html', {'produtos': produtos})

def cadastra_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'admin/cadastra_produto.html', {'form': form})

def edita_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'admin/cadastra_produto.html', {'form': form})

def deleta_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.delete()
    return redirect('lista_produtos')
