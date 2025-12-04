from django.contrib import admin
from django.utils.html import mark_safe
from .models import Produto, Pedido, ItemPedido, Cliente, Categoria

# --- PERSONALIZAÇÃO DO CABEÇALHO ---
admin.site.site_header = "Administração Socina"
admin.site.site_title = "Socina Admin"
admin.site.index_title = "Bem-vindo ao Gerenciamento da Loja"

# --- REGISTRO DA CATEGORIA (ESSENCIAL PARA O DROPDOWN) ---
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# --- PRODUTOS ---
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ver_imagem', 'nome', 'preco', 'quantidade_estoque', 'categoria')
    search_fields = ('nome',)
    list_filter = ('quantidade_estoque', 'categoria') 
    list_display_links = ('id', 'nome', 'ver_imagem')

    def ver_imagem(self, obj):
        if obj.imagem:
            return mark_safe(f'<img src="{obj.imagem.url}" width="60" height="60" style="object-fit:cover; border-radius:5px;" />')
        return "Sem imagem"
    ver_imagem.short_description = "Foto"

# --- PEDIDOS ---
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)
    can_delete = True

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nome', 'data', 'total', 'status', 'valor_frete')
    list_filter = ('status', 'data')
    search_fields = ('cliente__usuario__username', 'id')
    inlines = [ItemPedidoInline]

    def cliente_nome(self, obj):
        if obj.cliente and obj.cliente.usuario:
            return obj.cliente.usuario.username
        return "Cliente desconhecido"
    cliente_nome.short_description = "Cliente"

# --- OUTROS REGISTROS ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'endereco')

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'subtotal')