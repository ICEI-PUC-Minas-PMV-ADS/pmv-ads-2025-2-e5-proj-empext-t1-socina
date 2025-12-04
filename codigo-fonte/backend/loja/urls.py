from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- A MUDANÇA ESTÁ AQUI ---
    # Colocamos o admin.site.urls na rota vazia ''
    # Isso faz a tela de Login Azul ser a página principal do site.
    path('', admin.site.urls),

    # --- ROTAS DA LOJA (Continuam funcionando se digitar o link) ---
    path('catalogo/', views.catalogo, name='catalogo'),
    path('produto/<int:pk>/', views.produto_detalhe_view, name='produto_detalhe'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('pedido/finalizar/', views.finalizar_pedido_whatsapp, name='finalizar_pedido'),

    # --- OUTROS LOGINS (Do cliente) ---
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login-cliente/', views.login_view, name='login'), # Mudei o nome pra não conflitar com o admin
    path('logout/', views.logout_view, name='logout'),

    # --- SEU DASHBOARD PERSONALIZADO ---
    # Se você quiser acessar aquele painel com gráficos que fizemos:
    path('painel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('painel/relatorio/exportar/', views.exportar_relatorio_csv, name='exportar_relatorio_csv'),
    
    # --- CRUD RÁPIDO ---
    path('painel/produtos/', views.lista_produtos, name='lista_produtos'),
    path('painel/produtos/cadastrar/', views.cadastra_produto, name='cadastra_produto'),
]

# Configuração para servir imagens (Media)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)