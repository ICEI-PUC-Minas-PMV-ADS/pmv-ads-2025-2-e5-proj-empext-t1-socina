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

# Imports dos seus Modelos e Formulários
from .models import Produto, Pedido, ItemPedido, Cliente
from .forms import ProdutoForm

# --- HOME AGORA É O ADMIN ---
def home(request):
    """
    Quando o usuário acessar a raiz do site (socina.onrender.com),
    ele será enviado imediatamente para a tela de login do Admin (/admin/).
    """
    return redirect('/admin/')

# --- PÁGINAS DO CLIENTE ---
def catalogo(request):
    produtos = Produto.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'catalogo.html', {'produtos': produtos})

def produto_detalhe_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produto_detalhe.html', {'produto': produto})

# --- AUTENTICAÇÃO (CLIENTES) ---
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
    # Ao sair, volta para a home (que vai mandar para o admin login)
    return redirect('home')

# --- CARRINHO E CHECKOUT ---
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    subtotal_pedido = Decimal('0.0')
    
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
            continue

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

def finalizar_pedido_whatsapp(request):
    if not request.user.is_authenticated:
        return redirect('login')

    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('catalogo')

    valor_frete = Decimal(request.session.get('valor_frete', '0.0'))

    try:
        with transaction.atomic():
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
                prod = item['produto']
                prod.quantidade_estoque -= item['qtd']
                prod.save()

            del request.session['carrinho']
            if 'valor_frete' in request.session:
                del request.session['valor_frete']

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
            link_zap = f"https://wa.me/{numero_whatsapp}?text={texto_encoded}"
            
            return redirect(link_zap)

    except Exception as e:
        messages.error(request, f"Erro ao processar pedido: {e}")
        return redirect('ver_carrinho')

# --- FUNCIONALIDADES EXTRAS (DASHBOARD/EXPORTAR) ---
@staff_member_required
def admin_dashboard_view(request):
    total_pedidos = Pedido.objects.count()
    pedidos_concluidos = Pedido.objects.filter(status='concluido')
    total_vendas_valor = pedidos_concluidos.aggregate(Sum('total'))['total__sum'] or 0
    total_vendas_qtd = pedidos_concluidos.count()

    vendas_mensais = (
        Pedido.objects.filter(status='concluido')
        .annotate(mes=TruncMonth('data'))
        .values('mes').annotate(faturamento=Sum('total')).order_by('mes')
    )
    labels = [v['mes'].strftime('%m/%Y') for v in vendas_mensais if v['mes']]
    data = [float(v['faturamento']) for v in vendas_mensais if v['mes']]

    contexto = {
        'total_pedidos': total_pedidos,
        'total_vendas_qtd': total_vendas_qtd,
        'total_vendas_valor': total_vendas_valor,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    return render(request, 'admin/dashboard.html', contexto)

@staff_member_required
def exportar_relatorio_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Cliente', 'Data', 'Total', 'Status'])
    for p in Pedido.objects.all().order_by('-data'):
        cli = p.cliente.usuario.username if p.cliente and p.cliente.usuario else "Anônimo"
        writer.writerow([p.id, cli, p.data, p.total, p.status])
    return response

# Views de CRUD legadas (Opcionais se usar só o Admin)
@staff_member_required
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'admin/lista_produtos.html', {'produtos': produtos})

@staff_member_required
def cadastra_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid(): form.save(); return redirect('lista_produtos')
    else: form = ProdutoForm()
    return render(request, 'admin/cadastra_produto.html', {'form': form})

@staff_member_required
def edita_produto(request, pk):
    p = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=p)
        if form.is_valid(): form.save(); return redirect('lista_produtos')
    else: form = ProdutoForm(instance=p)
    return render(request, 'admin/cadastra_produto.html', {'form': form})

@staff_member_required
def deleta_produto(request, pk):
    get_object_or_404(Produto, pk=pk).delete()
    return redirect('lista_produtos')