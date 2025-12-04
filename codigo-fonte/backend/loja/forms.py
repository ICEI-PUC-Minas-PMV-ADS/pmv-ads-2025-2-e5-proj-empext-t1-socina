from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'imagem', 'preco', 'quantidade_estoque', 'categoria']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalhes do produto...'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            
            # ISSO AQUI FAZ VIRAR LISTA SUSPENSA COM BOOTSTRAP
            'categoria': forms.Select(attrs={'class': 'form-select'}), 
            
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
    # Garante que o campo categoria apareça com rótulo correto
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Selecione uma categoria..."