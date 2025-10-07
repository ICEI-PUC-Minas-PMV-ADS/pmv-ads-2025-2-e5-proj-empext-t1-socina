from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Páginas do Cliente
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),

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

    # Django Admin (nativo)
    path('admin/', admin.site.urls),
]