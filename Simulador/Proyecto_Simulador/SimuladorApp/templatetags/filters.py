from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def split(value1,value2):

	
	return value1.split(value2)


@register.filter(is_safe=True)
def translate(value1):

	res = None
	dict_translate = {
		'address_src':"Dirección del Salto",
		'address_dts' : "Dirección destino",
		'bits': "Contador",
		'was_jump': "Hay salto"
	}
	try:
		
		res = dict_translate[value1]

	except:

		res = value1

	
	return res
