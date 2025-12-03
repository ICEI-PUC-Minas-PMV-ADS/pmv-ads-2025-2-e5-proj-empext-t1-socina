from django.db import models
from django.contrib.auth.models import User

# --- NOVA TABELA DE CATEGORIAS ---
class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.usuario.username

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    quantidade_estoque = models.IntegerField()
    
    # MUDANÇA AQUI: Agora liga com a tabela Categoria
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"