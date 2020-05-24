
from io import BytesIO
import pandas as pd
from django.http import StreamingHttpResponse



def create_csv_response(df):
	
	sio = BytesIO()
	PandasDataFrame = df
	csv_res = PandasDataFrame.to_csv(index = None, header=True,sep=';',encoding='utf-8-sig',decimal=',')
	print(csv_res)


	response = StreamingHttpResponse(csv_res, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=%s.csv' % "resultados" 

	return response

def get_row_result(code_row,resultados):


	list_row = resultados[code_row.split("__")[-1]]
	row_result = list_row[code_row] 
	return row_result


def convert_to_data_frame(resultados_download):

	columns = resultados_download[0].keys()
	data = [result.values() for result in resultados_download]
	df = pd.DataFrame(data,columns=columns)

	return df
	

def download_file(request):
	print(request.POST)
	resultados = request.session.get('resultados')
	resultados_send = request.POST.getlist('resultados')

	
	resultados_download = [get_row_result(code_row,resultados) for code_row in resultados_send]
	df = convert_to_data_frame(resultados_download)
	

	return create_csv_response(df)