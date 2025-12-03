from django.contrib import admin
from .models import Produto, Cliente, Pedido, ItemPedido

# -----------------------------------------------------
# 1. ADMIN INLINE para ver Itens do Pedido
# -----------------------------------------------------
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0  # Não mostra linhas vazias extras
    readonly_fields = ('produto', 'quantidade', 'subtotal') # Opcional: evita edição acidental

# -----------------------------------------------------
# 2. ADMIN REGISTERS
# -----------------------------------------------------

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Exibe colunas importantes
    list_display = ("nome", "preco", "quantidade_estoque") 
    
    # IMPORTANTE: A vírgula no final é OBRIGATÓRIA para o Python entender que é uma tupla
    list_filter = ("preco",) 
    
    search_fields = ("nome", "descricao")

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "endereco")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Adiciona a lista de itens dentro do pedido
    inlines = [
        ItemPedidoInline,
    ]
    list_display = ("id", "cliente", "data", "status", "total")
    list_filter = ("status", "data")
    search_fields = ("cliente__usuario__username", "id")

# ItemPedido já aparece dentro de Pedido, então não precisa de registro isolado.