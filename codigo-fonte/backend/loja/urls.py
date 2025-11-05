from django.contrib import admin
from django.urls import path
from . import views

# Imports para servir arquivos de mídia em desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Páginas do Cliente
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    # Rota de Detalhe do Produto
    path('produto/<int:pk>/', views.produto_detalhe_view, name='produto_detalhe'),

    # Autenticação de Cliente
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Carrinho e Pedido
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('pedido/finalizar/', views.finalizar_pedido, name='finalizar_pedido'),

    # CRUD de produtos (Admin)
    path('admin/produtos/', views.lista_produtos, name='lista_produtos'),
    path('admin/produtos/cadastrar/', views.cadastra_produto, name='cadastra_produto'),
    path('admin/produtos/editar/<int:pk>/', views.edita_produto, name='edita_produto'),
    path('admin/produtos/deletar/<int:pk>/', views.deleta_produto, name='deleta_produto'),

    # --- ROTAS DO DASHBOARD QUE FALTAVAM ---
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/exportar-relatorio/', views.exportar_relatorio_csv, name='exportar_relatorio_csv'),

    # Django Admin (nativo)
    path('admin/', admin.site.urls),
]

# Adiciona a rota para servir arquivos de mídia (fotos dos produtos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)