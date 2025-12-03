from django import forms
from .models import Produto, Pedido

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'imagem', 'preco', 'quantidade_estoque', 'categoria']
        
        # Estilização para ficar bonito no HTML
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            # O Select cria a lista suspensa puxando do banco
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CEPForm(forms.Form):
    cep = forms.CharField(
        label='Calcular Frete (apenas números)',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: 30100000', 'class': 'border rounded py-2 px-3 text-gray-700'})
    )