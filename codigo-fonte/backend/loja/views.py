import json
import csv
import urllib.parse
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Produto, Pedido, ItemPedido, Cliente
from .forms import ProdutoForm

# --- PÁGINAS PÚBLICAS (CLIENTE NÃO PRECISA LOGAR) ---

def home(request):
    """
    Página Inicial do site.
    Se você não tiver um index.html, pode mudar para:
    return redirect('catalogo')
    """
    return render(request, 'index.html')

def catalogo(request):
    # Mostra todos os produtos com estoque
    produtos = Produto.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'catalogo.html', {'produtos': produtos})

def produto_detalhe_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produto_detalhe.html', {'produto': produto})

# --- AUTENTICAÇÃO ---

def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo') # Se já tá logado, vai pro catálogo
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Cria o perfil do cliente
            Cliente.objects.create(usuario=user, endereco="Não informado")
            login(request, user)
            # Redireciona para onde ele estava ou para o catálogo
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
            
            # Se ele veio do carrinho tentando comprar, manda de volta pro checkout
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- CARRINHO (PÚBLICO) ---

def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    subtotal_pedido = Decimal('0.0')
    
    # Lógica para recuperar produtos, mesmo se algum foi deletado
    carrinho_atualizado = carrinho.copy()
    
    for produto_id, quantidade in carrinho.items():
        try:
            produto = Produto.objects.get(id=int(produto_id))
            subtotal = produto.preco * quantidade
            subtotal_pedido += subtotal
            itens_carrinho.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal
            })
        except Produto.DoesNotExist:
            del carrinho_atualizado[produto_id]
    
    # Atualiza a sessão se removeu algo inválido
    if len(carrinho) != len(carrinho_atualizado):
        request.session['carrinho'] = carrinho_atualizado

    # Regra de Frete
    if not itens_carrinho:
        valor_frete = Decimal('0.0')
    elif subtotal_pedido >= 600:
        valor_frete = Decimal('0.0')
    else:
        valor_frete = Decimal('15.00')

    total_geral = subtotal_pedido + valor_frete
    request.session['valor_frete'] = str(valor_frete)

    contexto = {
        'itens_carrinho': itens_carrinho,
        'subtotal_pedido': subtotal_pedido,
        'valor_frete': valor_frete,
        'total_geral': total_geral,
        'frete_gratis': subtotal_pedido >= 600
    }
    return render(request, 'carrinho.html', contexto)

def adicionar_ao_carrinho(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    carrinho = request.session.get('carrinho', {})
    produto_id = str(pk)
    
    qtd_atual = carrinho.get(produto_id, 0)
    if qtd_atual + 1 <= produto.quantidade_estoque:
        carrinho[produto_id] = qtd_atual + 1
        request.session['carrinho'] = carrinho
        messages.success(request, f"{produto.nome} adicionado!")
    else:
        messages.warning(request, 'Estoque máximo atingido.')
        
    return redirect('ver_carrinho')

def remover_do_carrinho(request, pk):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(pk)
    if produto_id in carrinho:
        del carrinho[produto_id]
        request.session['carrinho'] = carrinho
    return redirect('ver_carrinho')

# --- CHECKOUT (SÓ LOGADO) ---

def finalizar_pedido_whatsapp(request):
    # AQUI ESTÁ A TRAVA: Se não estiver logado, manda pro login
    if not request.user.is_authenticated:
        # O parâmetro ?next faz ele voltar pra cá depois de logar
        return redirect('/login/?next=/pedido/finalizar/')

    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('catalogo')

    valor_frete = Decimal(request.session.get('valor_frete', '0.0'))

    try:
        with transaction.atomic():
            # Garante que o cliente existe
            cliente, created = Cliente.objects.get_or_create(
                usuario=request.user, 
                defaults={'endereco': 'Endereço não informado'}
            )

            subtotal_pedido = Decimal('0.0')
            itens_obj = []
            
            for produto_id, quantidade in carrinho.items():
                produto = Produto.objects.get(id=int(produto_id))
                subtotal = produto.preco * quantidade
                subtotal_pedido += subtotal
                itens_obj.append({'produto': produto, 'qtd': quantidade, 'sub': subtotal})
            
            total_geral = subtotal_pedido + valor_frete

            pedido = Pedido.objects.create(
                cliente=cliente,
                total=total_geral,
                valor_frete=valor_frete,
                status='em andamento' 
            )

            for item in itens_obj:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item['produto'],
                    quantidade=item['qtd'],
                    subtotal=item['sub']
                )
                # Baixa estoque
                prod = item['produto']
                prod.quantidade_estoque -= item['qtd']
                prod.save()

            # Limpa carrinho
            del request.session['carrinho']
            if 'valor_frete' in request.session:
                del request.session['valor_frete']

            # Gera texto WhatsApp
            texto = f"Olá! Acabei de fazer o pedido *#{pedido.id}* pelo site SOCINA. 💕\n\n"
            texto += "*Resumo do Pedido:*\n"
            for item in itens_obj:
                texto += f"▪ {item['produto'].nome} ({item['qtd']}x): R$ {item['sub']:.2f}\n"
            
            texto += "\n--------------------------------\n"
            texto += f"📦 Subtotal: R$ {subtotal_pedido:.2f}\n"
            texto += f"🚚 Frete: R$ {valor_frete:.2f}\n"
            texto += f"💰 *TOTAL: R$ {total_geral:.2f}*\n"
            texto += "\nAguardo a chave PIX para pagamento!"

            texto_encoded = urllib.parse.quote(texto)
            numero_whatsapp = "553192742082"
            return redirect(f"https://wa.me/{numero_whatsapp}?text={texto_encoded}")

    except Exception as e:
        messages.error(request, f"Erro ao processar: {e}")
        return redirect('ver_carrinho')

# --- ÁREA ADM (DASHBOARD) ---
@staff_member_required
def admin_dashboard_view(request):
    # ... (Seu código do dashboard, não precisa mudar)
    # Só vou resumir aqui pra não ficar gigante, use o que já te mandei do dashboard
    total_pedidos = Pedido.objects.count()
    pedidos_concluidos = Pedido.objects.filter(status='concluido')
    total_vendas_valor = pedidos_concluidos.aggregate(Sum('total'))['total__sum'] or 0
    total_vendas_qtd = pedidos_concluidos.count()
    
    # ... (Lógica do gráfico) ...
    
    # Se precisar do código completo do dashboard de novo, me avise,
    # mas o importante aqui é manter o @staff_member_required
    return render(request, 'admin/dashboard.html', locals())

@staff_member_required
def exportar_relatorio_csv(request):
    # ... (Seu código de CSV, mantenha igual) ...
    return HttpResponse("Relatório") # Simplificado só pra caber na resposta

# --- CRUD LEGADO ---
@staff_member_required
def lista_produtos(request):
    return render(request, 'admin/lista_produtos.html', {'produtos': Produto.objects.all()})

@staff_member_required
def cadastra_produto(request):
    # ... (Seu código de cadastro, mantenha igual) ...
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid(): form.save(); return redirect('lista_produtos')
    else: form = ProdutoForm()
    return render(request, 'admin/cadastra_produto.html', {'form': form})