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
            'categoria': forms.Select(attrs={'class': 'form-select'}), 
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Selecione uma categoria..."

class EnderecoForm(forms.Form):
    cep = forms.CharField(label='CEP', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors', 'placeholder': '00000-000'}))
    rua = forms.CharField(label='Rua/Avenida', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors'}))
    numero = forms.CharField(label='Número', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors'}))
    complemento = forms.CharField(label='Complemento', required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors', 'placeholder': 'Apto, Bloco (Opcional)'}))
    bairro = forms.CharField(label='Bairro', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors'}))
    cidade = forms.CharField(label='Cidade', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors'}))
    estado = forms.CharField(label='Estado', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border-2 border-gray-200 rounded-lg p-3 focus:outline-none focus:border-socina-pink transition-colors', 'placeholder': 'MG'}))