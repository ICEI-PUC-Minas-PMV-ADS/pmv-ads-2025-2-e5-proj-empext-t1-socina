from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- ROTA HOME (Pública) ---
    path('', views.home, name='home'),

    # --- DJANGO ADMIN (Acesso da Dona) ---
    path('admin/', admin.site.urls),

    # --- LOJA / CLIENTE (Público) ---
    path('catalogo/', views.catalogo, name='catalogo'),
    path('produto/<int:pk>/', views.produto_detalhe_view, name='produto_detalhe'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('pedido/finalizar/', views.finalizar_pedido_whatsapp, name='finalizar_pedido'),

    # --- LOGIN / CADASTRO ---
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- DASHBOARD PERSONALIZADO (Acesso Rápido) ---
    path('painel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('painel/relatorio/exportar/', views.exportar_relatorio_csv, name='exportar_relatorio_csv'),
    
    # --- TELAS EXTRAS DE CADASTRO (Opcionais, mantive pois seu dashboard usa) ---
    path('painel/produtos/', views.lista_produtos, name='lista_produtos'),
    path('painel/produtos/cadastrar/', views.cadastra_produto, name='cadastra_produto'),
    
    # REMOVI AS ROTAS DE EDITAR E DELETAR QUE DAVAM ERRO
    # A edição e exclusão devem ser feitas entrando em /admin/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)