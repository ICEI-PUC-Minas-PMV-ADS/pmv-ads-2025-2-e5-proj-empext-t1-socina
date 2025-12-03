from django.contrib import admin
from .models import Produto, Pedido, ItemPedido, Cliente

# Configuração para mostrar itens DENTRO do pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data', 'total', 'status')
    list_filter = ('status', 'data')
    inlines = [ItemPedidoInline]

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade_estoque')
    search_fields = ('nome',)

# Registra os outros modelos simples
admin.site.register(Cliente)
admin.site.register(ItemPedido)