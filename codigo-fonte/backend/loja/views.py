from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal
import urllib.parse 
import csv
from django.http import HttpResponse

# Imports dos seus Modelos e Formulários
from .models import Produto, Pedido, ItemPedido, Cliente
from .forms import ProdutoForm

# --- Páginas Públicas ---
def home(request):
    return render(request, 'index.html')

def catalogo(request):
    produtos = Produto.objects.filter(quantidade_estoque__gt=0)
    return render(request, 'catalogo.html', {'produtos': produtos})

def produto_detalhe_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produto_detalhe.html', {'produto': produto})

# --- Autenticação ---
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

# --- Carrinho e Finalização ---
def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    subtotal_pedido = Decimal('0.0')
    
    # Busca produtos e calcula subtotal
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id))
        subtotal = produto.preco * quantidade
        subtotal_pedido += subtotal
        itens_carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

    # Lógica de Frete (Grátis acima de 600, senão 15.00)
    if not itens_carrinho:
        valor_frete = Decimal('0.0')
    elif subtotal_pedido >= 600:
        valor_frete = Decimal('0.0')
    else:
        valor_frete = Decimal('15.00')

    total_geral = subtotal_pedido + valor_frete

    # Salva valores na sessão para usar na finalização
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
    
    # Lógica simples de estoque
    qtd_atual = carrinho.get(produto_id, 0)
    if qtd_atual + 1 <= produto.quantidade_estoque:
        carrinho[produto_id] = qtd_atual + 1
        request.session['carrinho'] = carrinho
    else:
        messages.warning(request, 'Estoque máximo atingido para este item.')
        
    return redirect('ver_carrinho')

def remover_do_carrinho(request, pk):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(pk)
    if produto_id in carrinho:
        del carrinho[produto_id]
        request.session['carrinho'] = carrinho
    return redirect('ver_carrinho')

def finalizar_pedido_whatsapp(request):
    """
    Salva o pedido no banco de dados e redireciona para o WhatsApp.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return redirect('catalogo')

    valor_frete = Decimal(request.session.get('valor_frete', '0.0'))

    try:
        with transaction.atomic():
            # 1. Garante que o cliente existe
            cliente, created = Cliente.objects.get_or_create(
                usuario=request.user, 
                defaults={'endereco': 'Endereço não informado'}
            )

            # 2. Recalcula totais (segurança)
            subtotal_pedido = Decimal('0.0')
            itens_obj = [] # Lista temporária para montar a msg do Zap
            
            for produto_id, quantidade in carrinho.items():
                produto = Produto.objects.get(id=int(produto_id))
                subtotal = produto.preco * quantidade
                subtotal_pedido += subtotal
                itens_obj.append({'produto': produto, 'qtd': quantidade, 'sub': subtotal})
            
            total_geral = subtotal_pedido + valor_frete

            # 3. Cria o Pedido no Banco
            pedido = Pedido.objects.create(
                cliente=cliente,
                total=total_geral,
                valor_frete=valor_frete,
                status='em andamento' # Ou 'Pendente Pagamento'
            )

            # 4. Cria os Itens e Baixa Estoque
            for item in itens_obj:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item['produto'],
                    quantidade=item['qtd'],
                    subtotal=item['sub']
                )
                # Baixa no estoque
                prod = item['produto']
                prod.quantidade_estoque -= item['qtd']
                prod.save()

            # 5. Limpa Sessão
            del request.session['carrinho']
            del request.session['valor_frete']

            # 6. Monta Mensagem do WhatsApp
            texto = f"Olá! Acabei de fazer o pedido *#{pedido.id}* pelo site SOCINA. 💕\n\n"
            texto += "*Resumo do Pedido:*\n"
            
            for item in itens_obj:
                texto += f"▪ {item['produto'].nome} ({item['qtd']}x): R$ {item['sub']:.2f}\n"
            
            texto += "\n--------------------------------\n"
            texto += f"📦 Subtotal: R$ {subtotal_pedido:.2f}\n"
            
            if valor_frete == 0:
                texto += "🚚 Frete: GRÁTIS\n"
            else:
                texto += f"🚚 Frete: R$ {valor_frete:.2f}\n"
                
            texto += f"💰 *TOTAL: R$ {total_geral:.2f}*\n"
            texto += "\nAguardo a chave PIX para pagamento!"

            # 7. Redireciona
            texto_encoded = urllib.parse.quote(texto)
            numero_whatsapp = "5531971741924" # <--- INSIRA O NÚMERO CORRETO AQUI
            link_zap = f"https://wa.me/{numero_whatsapp}?text={texto_encoded}"
            
            return redirect(link_zap)

    except Exception as e:
        messages.error(request, f"Erro ao processar pedido: {e}")
        return redirect('ver_carrinho')

# --- CRUD Admin (Mantido igual) ---
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

@staff_member_required
def exportar_relatorio_csv(request):
    """
    Gera um arquivo CSV com todos os pedidos para a dona baixar.
    """
    # Cria a resposta do tipo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_vendas_socina.csv"'

    writer = csv.writer(response)
    # Cabeçalho das colunas
    writer.writerow(['ID Pedido', 'Cliente', 'Data', 'Status', 'Frete', 'Total', 'Produtos'])

    # Busca os pedidos
    pedidos = Pedido.objects.all().order_by('-data')

    for pedido in pedidos:
        # Cria uma lista de produtos num texto só (ex: "Camisa (2), Calça (1)")
        itens_str = ", ".join([f"{item.produto.nome} ({item.quantidade})" for item in pedido.itens.all()])
        
        # Formata a data
        data_formatada = pedido.data.strftime('%d/%m/%Y %H:%M')

        writer.writerow([
            pedido.id,
            pedido.cliente.usuario.username,
            data_formatada,
            pedido.get_status_display(),
            pedido.valor_frete,
            pedido.total,
            itens_str
        ])

    return response