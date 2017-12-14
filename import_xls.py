import json
from openpyxl import Workbook, load_workbook
import datetime

def get_time(param):
	now = datetime.datetime.now()
	str_time = str(now.strftime('%Y-%m-%d'))
	str_date = str(now.strftime('%H:%M:%S'))
	if param:
		return str_time
	else:
		return str_date

def load_data():
	wb = load_workbook(filename = 'report.xlsx')
	sheet_ranges = wb['consignors']
	alph = 'ABCDEFGHIJKLMN'
	current_value = sheet_ranges['A2'].value
	#for row in range(2, 20):
	row = 2
	#value = {}
	j = 1
	new_data={}
	while current_value != None:
		value = {}
		#new_data={}
		i = 0

		for col in alph:
			print(sheet_ranges[col + str(row)].value)
			#try:
			if str(sheet_ranges[col + str(row)].value) == None:
				present_value = ' '
			else:
				present_value = str(sheet_ranges[col + str(row)].value)
			#except:
			#present_value = ' '
			if i==7: issued_time = present_value
			if i==8: issued_date = present_value
			if i==9: delivered_time = present_value
			if i==10: delivered_date = present_value
			if i==11: delivering_time = present_value
			if i==12: delivering_date = present_value
			if i==0: OrderNum = present_value
			if i==1: point_DPD = present_value
			if i==2: point_Pulse = check_point(present_value)
			if i==3: ParcelNum = present_value
			if i==4: time_p = present_value
			if i==5: 
				num = present_value.find('00:00:00')
				if num!= -1:
					date_p = present_value[:num-1]
				else:
					date_p = present_value
			if i==6: 
				consignor = present_value
				#point_Pulse = check_point(point_Pulse_temp)
			if i==13: 
				ref = present_value
				try:
					value = {
						'dpd_order': OrderNum,
						'parcelNum:': ParcelNum, 
						'Time': time_p, 
						'stationNums': point_DPD,
						'Date': date_p,
						'pointCode': point_Pulse,
						'consignor': consignor,
						'issued_time': issued_time,
						'issued_date': issued_date,
						'delivered_time': delivered_time,
						'delivered_date': delivered_date,
						'delivering_time': delivering_time,
						'delivering_date': delivering_date,
						'ref': ref					
					}
				except:
					value = {
						'dpd_order': OrderNum,
						'parcelNum:': ParcelNum, 
						'Time': time_p, 
						'stationNums': point_DPD,
						'Date': date_p,
						'pointCode': point_Pulse,
						'consignor': consignor
						}					
				new_data.update([(j, value)])
				#print(j)
				#value.clear()
			i += 1


		#value.update([('stationNums', point_DPD)])
		#value.update([('pointCode', point_Pulse)])
		#value.update([('parcelNum:', ParcelNum)])
		#value.update([('Time', time_p)])
		#value.update([('Date', date_p)])
		#value.update([('consignor', consignor)])
		
		#save_in(OrderNum, value)
		new_data['count'] = j


		row += 1
		j += 1
		current_value = sheet_ranges['A' + str(row)].value
		print('/t', current_value)
	puth = 'consignors_dumps.json'
	with open(puth, 'w') as filek:
		json.dump(new_data, filek, ensure_ascii=False)
	puth_v = 'consignors.json'
	with open(puth_v, 'w') as filek_v:
		json.dump(new_data, filek_v, ensure_ascii=False)
	wb.close()
	print(row)


def check_point(points):
	#if points == '9999': return points
	lengths = len(points)
	#flag = points.find()
	if lengths == 4: return points 
	if lengths == 3: 
		fact_point = '0' + points
		return fact_point
	if lengths == 2:
		fact_point = '00' + points
		return fact_point
	if lengths == 1:
		fact_point = '000' + points
		return fact_point
	if (lengths != 4) or (lengths != 3) or (lengths != 2):
		return points
def save_in(dpdOrderNum, value):
	date_current = get_time(True)
	puth = 'consignors_finish.json'
	try:
		with open(puth) as file:
			datas = json.load(file)
			file.close()
		with open(puth, 'w') as file:
			datas.update([(dpdOrderNum, value)])
			json.dump(datas, file, ensure_ascii=False)
			file.close()
	except:
		with open(puth, 'w') as file:
			value_header = {dpdOrderNum: {}}
			value_header.update([(dpdOrderNum, value)])
			json.dump(value_header, file, ensure_ascii=False)
			file.close()


if __name__ == '__main__':
	load_data()
