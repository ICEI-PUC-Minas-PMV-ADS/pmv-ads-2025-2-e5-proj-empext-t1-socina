from django.contrib import admin
from .models import Produto, Cliente, Pedido, ItemPedido

# -----------------------------------------------------
# 1. ADMIN INLINE para ver Itens do Pedido (Passo 2)
# -----------------------------------------------------
# Permite que a lista de ItemPedido apareça dentro da tela de Pedido.
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0  # Não mostra linhas vazias por padrão
    # Opcional: torna esses campos somente leitura para evitar edição acidental do preço/produto
    readonly_fields = ('produto', 'quantidade', 'subtotal') 

# -----------------------------------------------------
# 2. ADMIN REGISTERS
# -----------------------------------------------------

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Melhoria: Adiciona 'categoria' na lista de exibição (Passo 1)
    list_display = ("nome", "preco", "quantidade_estoque", "categoria") 
    # Adiciona filtros laterais
    list_filter = ("categoria", "em_promocao")
    search_fields = ("nome", "descricao")

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "endereco")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Melhoria: Adiciona o Inline para exibir os ItensPedido (Passo 2)
    inlines = [
        ItemPedidoInline,
    ]
    list_display = ("id", "cliente", "data", "status", "total")
    list_filter = ("status", "data")
    search_fields = ("cliente__usuario__username", "id")

# Remove o registro separado do ItemPedido, já que ele é exibido via Inline
# @admin.register(ItemPedido) 
# class ItemPedidoAdmin(admin.ModelAdmin):
#     list_display = ("pedido", "produto", "quantidade", "subtotal")