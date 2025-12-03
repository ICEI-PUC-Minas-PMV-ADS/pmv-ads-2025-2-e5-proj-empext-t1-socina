from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Páginas do Cliente
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('produto/<int:pk>/', views.produto_detalhe_view, name='produto_detalhe'),

    # Autenticação
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Carrinho e Checkout
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    
    # Rota Final (Salva no banco e manda pro Zap)
    path('pedido/finalizar/', views.finalizar_pedido_whatsapp, name='finalizar_pedido'),

    # Área Admin Customizada (CRUD)
    path('painel/produtos/', views.lista_produtos, name='lista_produtos'),
    path('painel/produtos/cadastrar/', views.cadastra_produto, name='cadastra_produto'),
    path('painel/produtos/editar/<int:pk>/', views.edita_produto, name='edita_produto'),
    path('painel/produtos/deletar/<int:pk>/', views.deleta_produto, name='deleta_produto'),

    # Django Admin (Jazzmin)
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)