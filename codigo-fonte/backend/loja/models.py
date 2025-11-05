from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.usuario.username

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    # NOVO CAMPO DE IMAGEM
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField()
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('em andamento', 'Em andamento'),
        ('concluído', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em andamento')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"