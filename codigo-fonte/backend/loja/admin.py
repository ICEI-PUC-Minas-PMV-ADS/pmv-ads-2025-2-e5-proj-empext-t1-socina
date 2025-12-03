from django.contrib import admin
from django.utils.html import mark_safe # Necessário para renderizar a imagem HTML
from .models import Produto, Pedido, ItemPedido, Cliente

# --- PERSONALIZAÇÃO DO CABEÇALHO DO ADMIN ---
admin.site.site_header = "Administração Socina"
admin.site.site_title = "Socina Admin"
admin.site.index_title = "Bem-vindo ao Gerenciamento da Loja"

# --- CONFIGURAÇÃO DE PRODUTOS ---
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista
    list_display = ('id', 'ver_imagem', 'nome', 'preco', 'quantidade_estoque')
    
    # Campo de busca (pesquisa por nome)
    search_fields = ('nome',)
    
    # Filtro lateral (por estoque)
    list_filter = ('quantidade_estoque',)
    
    # Campos que podem ser clicados para entrar na edição
    list_display_links = ('id', 'nome', 'ver_imagem')

    # Função para exibir a miniatura da imagem
    def ver_imagem(self, obj):
        if obj.imagem:
            # Cria uma tag HTML <img> segura
            return mark_safe(f'<img src="{obj.imagem.url}" width="60" height="60" style="object-fit:cover; border-radius:5px;" />')
        return "Sem imagem"
    
    # Nome da coluna na tabela
    ver_imagem.short_description = "Foto"

# --- CONFIGURAÇÃO DE PEDIDOS ---

# Configuração para mostrar itens DENTRO do pedido (Inline)
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0 # Não mostra linhas vazias extras sem necessidade
    readonly_fields = ('subtotal',) # O subtotal é calculado, melhor não editar manualmente
    can_delete = True # Permite deletar um item do pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Colunas da tabela de pedidos
    list_display = ('id', 'cliente_nome', 'data', 'total', 'status', 'valor_frete')
    
    # Filtros laterais úteis
    list_filter = ('status', 'data')
    
    # Barra de pesquisa (busca pelo nome do usuário do cliente)
    search_fields = ('cliente__usuario__username', 'id')
    
    # Adiciona os itens dentro da tela do pedido
    inlines = [ItemPedidoInline]

    # Helper para mostrar o nome do cliente na tabela
    def cliente_nome(self, obj):
        if obj.cliente and obj.cliente.usuario:
            return obj.cliente.usuario.username
        return "Cliente desconhecido"
    cliente_nome.short_description = "Cliente"

# --- CONFIGURAÇÃO DE CLIENTES ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'endereco')
    search_fields = ('usuario__username', 'endereco')

# O ItemPedido já aparece dentro de Pedido, mas se quiser ver a lista completa separada:
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'subtotal')
    list_filter = ('pedido__data',)