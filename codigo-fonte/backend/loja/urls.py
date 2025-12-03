from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- PÁGINAS DO CLIENTE ---
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('produto/<int:pk>/', views.produto_detalhe_view, name='produto_detalhe'),

    # --- AUTENTICAÇÃO ---
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- CARRINHO E CHECKOUT ---
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('pedido/finalizar/', views.finalizar_pedido_whatsapp, name='finalizar_pedido'),

    # --- ÁREA DE GESTÃO (DASHBOARD E RELATÓRIOS) ---
    # Rota para ver os gráficos e indicadores
    path('painel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    # Rota para baixar o Excel/CSV
    path('painel/relatorio/exportar/', views.exportar_relatorio_csv, name='exportar_relatorio_csv'),

    # --- CRUD DE PRODUTOS (ADMIN PERSONALIZADO) ---
    path('painel/produtos/', views.lista_produtos, name='lista_produtos'),
    path('painel/produtos/cadastrar/', views.cadastra_produto, name='cadastra_produto'),
    path('painel/produtos/editar/<int:pk>/', views.edita_produto, name='edita_produto'),
    path('painel/produtos/deletar/<int:pk>/', views.deleta_produto, name='deleta_produto'),

    # --- DJANGO ADMIN (JAZZMIN) ---
    path('admin/', admin.site.urls),
]

# Serve arquivos de mídia no modo DEBUG (Desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
