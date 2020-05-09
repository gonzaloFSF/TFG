from django import forms

TIPO_REMPLAZO = [	
	(1, 'Remplazo lru'),
	(0, 'Remplazo aleatorio')
	]

class BTBForm(forms.Form):

	is_lru = forms.CharField(required=False,label='Remplazo lru',widget=forms.RadioSelect(attrs={'class':'radio-inline'}, choices=TIPO_REMPLAZO))
	size_buffer = forms.CharField(required=False,label='Numero de entradas del buffer',widget=forms.NumberInput(attrs={'class':'form-control'}))
	num_pred_bits = forms.CharField(required=False,label='Numero de bits de prediccion',widget=forms.NumberInput(attrs={'class':'form-control'}))
	init_bits_value = forms.CharField(required=False,label='Prediccion inial',widget=forms.NumberInput(attrs={'class':'form-control'}))


class UploadFileForm(forms.Form):

	title = forms.CharField(label='Nombre [arg1 arg2 ...]',max_length=50)
	file = forms.FileField(label='Codigo a subir',widget=forms.FileInput(attrs={'class':'btn btn-success'}))
		