from django import forms

TIPO_REMPLAZO = [    
    ('LRU', 'Remplazo lru'),
    ('ALE', 'Remplazo aleatorio')
    ]

class BTBForm(forms.Form):

    is_lru = forms.CharField(label='Remplazo lru',widget=forms.RadioSelect(attrs={'class':'radio-inline'}, choices=TIPO_REMPLAZO))
    buffer_size = forms.CharField(label='Numero de entradas del buffer',widget=forms.TextInput(attrs={'class':'form-control'}))
    num_pred_bits = forms.CharField(label='Numero de bits de prediccion',widget=forms.TextInput(attrs={'class':'form-control'}))
    init_bits_value = forms.CharField(label='Prediccion inial',widget=forms.TextInput(attrs={'class':'form-control'}))


        