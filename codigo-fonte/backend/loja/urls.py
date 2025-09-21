from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Catálogo
    path('catalogo/', views.catalogo, name='catalogo'),

    # CRUD de produtos personalizado
    path('admin/produtos/', views.lista_produtos, name='lista_produtos'),
    path('admin/produtos/cadastrar/', views.cadastra_produto, name='cadastra_produto'),
    path('admin/produtos/editar/<int:pk>/', views.edita_produto, name='edita_produto'),
    path('admin/produtos/deletar/<int:pk>/', views.deleta_produto, name='deleta_produto'),

    # Pedido
    path('pedido/criar/', views.cria_pedido, name='cria_pedido'),

    # Django Admin (nativo)
    path('admin/', admin.site.urls),
]
