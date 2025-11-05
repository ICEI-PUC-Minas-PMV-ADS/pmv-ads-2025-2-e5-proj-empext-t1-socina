from django import forms
from .models import Produto, Pedido

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # ADICIONADO 'imagem'
        fields = ['nome', 'descricao', 'imagem', 'preco', 'quantidade_estoque', 'categoria']

class CEPForm(forms.Form):
    cep = forms.CharField(
        label='Calcular Frete (apenas números)',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: 30100000', 'class': 'border rounded py-2 px-3 text-gray-700'})
    )