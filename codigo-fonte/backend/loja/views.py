from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from decimal import Decimal

# Imports para o Dashboard e Relatórios
import csv
import json
from django.http import HttpResponse
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

# Imports dos seus Modelos e Formulários
from .models import Produto, Pedido, ItemPedido, Cliente
from .forms import ProdutoForm, CEPForm

# --- Páginas Públicas ---
def home(request):
    return render(request, 'index.html')

def catalogo(request):
    produtos = Produto.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'catalogo.html', {'produtos': produtos})

def produto_detalhe_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    contexto = {
        'produto': produto
    }
    return render(request, 'produto_detalhe.html', contexto)

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


# --- Lógica do Carrinho e Frete Fixo ---
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    subtotal_pedido = Decimal('0.0')
    
    valor_frete = Decimal('15.50') # Nosso frete fixo
    
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id))
        subtotal = produto.preco * quantidade
        itens_carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        subtotal_pedido += subtotal

    if not itens_carrinho:
        valor_frete = Decimal('0.0') 

    request.session['valor_frete'] = str(valor_frete)
    total_geral = subtotal_pedido + valor_frete

    contexto = {
        'itens_carrinho': itens_carrinho,
        'subtotal_pedido': subtotal_pedido,
        'valor_frete': valor_frete,
        'total_geral': total_geral,
        'cep_form': None, 
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
    valor_frete = Decimal(str(request.session.get('valor_frete', '0.0')))

    if not carrinho:
        return redirect('catalogo')

    try:
        with transaction.atomic():
            
            # --- AQUI ESTÁ A CORREÇÃO ---
            # Em vez de .get(), usamos .get_or_create().
            # Isso busca o perfil do cliente. Se não existir (ex: é um admin),
            # ele cria um perfil de cliente na hora.
            cliente, created = Cliente.objects.get_or_create(
                usuario=request.user, 
                defaults={'endereco': 'Endereço Admin/Não informado'}
            )
            # --- FIM DA CORREÇÃO ---

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
                produto.save() # Baixa no estoque

            del request.session['carrinho']
            del request.session['valor_frete']
            
            # Agora sim, você será enviado para a página de confirmação!
            return render(request, 'pedido_confirmado.html', {'pedido': pedido})

    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return redirect('ver_carrinho')


# --- CRUD de Produtos (Admin) ---
@staff_member_required
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'admin/lista_produtos.html', {'produtos': produtos})

@staff_member_required
def cadastra_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'admin/cadastra_produto.html', {'form': form})

@staff_member_required
def edita_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'admin/cadastra_produto.html', {'form': form})

@staff_member_required
def deleta_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.delete()
    return redirect('lista_produtos')

# --- Dashboard e Relatório (Admin) ---
@staff_member_required
def admin_dashboard_view(request):
    vendas_por_mes = (
        Pedido.objects
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total_vendido=Sum('total'))
        .order_by('mes')
    )
    
    labels_py = [venda['mes'].strftime('%B/%Y') for venda in vendas_por_mes]
    data_py = [float(venda['total_vendido']) for venda in vendas_por_mes]
    
    labels = json.dumps(labels_py)
    data = json.dumps(data_py)
    
    total_vendas_geral = Pedido.objects.aggregate(Sum('total'))['total__sum'] or 0
    total_pedidos = Pedido.objects.count()

    contexto = {
        'labels': labels,
        'data': data,
        'total_vendas_geral': total_vendas_geral,
        'total_pedidos': total_pedidos,
    }
    return render(request, 'admin/dashboard.html', contexto)

@staff_member_required
def exportar_relatorio_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="relatorio_vendas_{timezone.now().strftime("%Y-%m-%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID Pedido', 'Cliente', 'Data', 'Status', 'Valor Frete', 'Total'])
    
    pedidos = Pedido.objects.all().select_related('cliente__usuario')
    for pedido in pedidos:
        writer.writerow([
            pedido.id,
            pedido.cliente.usuario.username,
            pedido.data.strftime('%Y-%m-%d %H:%M'),
            pedido.get_status_display(),
            pedido.valor_frete,
            pedido.total
        ])
        
    return response