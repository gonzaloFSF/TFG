from django import forms

TIPO_REMPLAZO = [    
    (1, 'Remplazo lru'),
    (0, 'Remplazo aleatorio')
    ]

class BTBForm(forms.Form):

    is_lru = forms.CharField(label='Remplazo lru',widget=forms.RadioSelect(attrs={'class':'radio-inline'}, choices=TIPO_REMPLAZO))
    size_buffer = forms.CharField(label='Numero de entradas del buffer',widget=forms.NumberInput(attrs={'class':'form-control'}))
    num_pred_bits = forms.CharField(label='Numero de bits de prediccion',widget=forms.NumberInput(attrs={'class':'form-control'}))
    init_bits_value = forms.CharField(label='Prediccion inial',widget=forms.NumberInput(attrs={'class':'form-control'}))
    predictor_id = forms.CharField(label='',widget=forms.TextInput(attrs={'value':'pred_btb','style':'display:none'}))


        