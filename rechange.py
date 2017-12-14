import datetime
import json
import time

def changed_json_files():
	puth = 'consignors_recon.json'
	flag = True
	try:
		with open(puth) as file:
			data = json.load(file)
		for keys in data.keys():
			print(data[keys])
			date_num = data[keys]['Date'].find('-')
			if date_num != -1:
				print('DATE OKAY')
				print(keys)
			else:
				print('DATE NE OKAY')
				flag = False
		if flag == True:
			print('Ok')
		else:
			print('Not ok')

	except:
		print('ERROR LOAD FILE')

def configured_data():
	#puth = 'consignors.json'
	puth2 = 'consignors_probka.json'
	with open(puth2) as file:
		data = json.load(file)
	new_data={}
	i = 1
	value = {}
	#for keys in data.keys():
	count = data['count']
	while i<count+1:
		print(data[str(i)])
		#print(keys)
		i +=1
	print(i-1)
	print(count)
		#value = {
		#		'dpd_order': keys,
		#		'parcelNum:': data[keys]['parcelNum:'], 
		#		'Time': data[keys]['Time'], 
		#		'stationNums': data[keys]['stationNums'],
		#		'Date': data[keys]['Date'],
		#		'pointCode': data[keys]['pointCode'],
		#		'consignor': data[keys]['consignor'] 
		#		}
		#defff = data[keys].get('parcelNum:')
		#if defff != None:
		#	print(keys, data[keys]['parcelNum:'])
		#else:
		#	pass
		#new_data.update([(str(i), value)])
		#value = {}
		#i +=1
		#print(i)
	#new_data['count'] = i
	#with open(puth2, 'w') as filek:
		#json.dump(new_data, filek, ensure_ascii=False)
def search_dubl():
	puth = 'consignors_new.json'
	puth2 = 'consignors_new_2.json'
	puth3 = 'consignors_finish.json'
	with open(puth) as file1:
		data1 = json.load(file1)
	file1.close()
	with open(puth2) as file2:
		data2 = json.load(file2)
	file2.close()
	count1 = data1['count']
	count2 = data2['count']
	i = 1
	j = 1

	while i<count2+1:
		flag = False
		perem_count = data1['count']
		while j<count1+1:
			if data1[str(j)]['parcelNum:'] == data2[str(i)]['parcelNum:']:
				flag = True
			else:
				flag = False
				thas = data2[str(i)]
			j +=1
		if flag == False:
			data1.update([('count', perem_count + 1)]) 
			data1.update([(perem_count+1, thas)])
		i+=1
	with open(puth3, 'w') as filek:
		json.dump(data1, filek, ensure_ascii=False)

if __name__ == '__main__':
	#changed_json_files()
	configured_data()
	#search_dubl()
