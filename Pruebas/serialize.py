import pickle





class A():

	b = None
	name = ""

	def __init__(self,b):
		
		self.b = b

	def ponme_name(self,name):

		self.name = name

	def __str__(self):

		print("b : {} \n\n\n\n\n\n\n\n\n\n\nname : {}".format(self.b,self.name))

class B():

	dict_attribute = {}
	string = None
	number = 83276387468746

	def __init__(self,dict_atribute,string,number):

		self.dict_atribute = dict_atribute
		self.string = string
		self.number = number

