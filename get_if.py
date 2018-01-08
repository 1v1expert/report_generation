import http.client
import datetime
import json
import time


def get_time(param):
	now = datetime.datetime.now()
	str_time = str(now.strftime('%Y-%m-%d'))
	str_date = str(now.strftime('%H:%M:%S'))
	if param:
		return str_time
	else:
		return str_date


def load_file_f():
	puth = 'consignors.json'
	puth_dumps = 'consignors_dumps.json'
	try:
		with open(puth) as filej:
			data12 = json.load(filej)
		filej.close()
		with open(puth_dumps) as filep:
			data21 = json.load(filep)
		filep.close()
		if data12['count'] < data21['count']:
			return data21
		else:
			return data12
	except:
		try:
			with open(puth_dumps) as filep:
				data21 = json.load(filep)
			filep.close()
			return data21
		except:
			paxa = dict()
			with open(puth, 'w') as fiiil:
				json.dump(paxa, fiiil, ensure_ascii=False)
			fiiil.close()
			return paxa


def load_file_d():
	puth = 'consignors_temp_' + str(get_time(True)) + 'json'
	puth_dumps = 'consignors_dumps_temp_' + str(get_time(True)) + '.json'
	try:
		with open(puth) as filej:
			data12 = json.load(filej)
		filej.close()
		with open(puth_dumps) as filep:
			data21 = json.load(filep)
		filep.close()
		if data12['count'] < data21['count']:
			return data21
		else:
			return data12
	except:
		try:
			with open(puth_dumps) as filep:
				data21 = json.load(filep)
			filep.close()
			return data21
		except:
			paxa = {}
			with open(puth, 'w') as fiiil:
				json.dump(paxa, fiiil, ensure_ascii=False)
			fiiil.close()
			return paxa


def rewritingg():
	datings = load_file_f()
	puth = 'consignors_temp_' + str(get_time(True)) + 'json'
	puth_dumps = 'consignors_dumps_temp_' + str(get_time(True)) + '.json'
	with open(puth, 'w') as fileq:
		json.dump(datings, fileq, ensure_ascii=False)
	fileq.close()
	with open(puth_dumps, 'w') as filet:
		json.dump(datings, filet, ensure_ascii=False)
	filet.close()


def get_parcel_pulse():
	conn = http.client.HTTPSConnection("api.pulse.express")
	conn_2 = http.client.HTTPSConnection("api.pulse.express")
	headers = {
		'content-type': "application/json",
		'authorization': ""
	}
	
	conn.request("GET", "/v1/parcels/?limit=300", headers=headers)
	
	res = conn.getresponse()
	data = res.read()
	conn.close()
	datal = json.loads(data.decode("utf-8"))
	keys = 0
	while keys < 300:
		parcelNums = None
		print(datal['results'][keys]['order_id'], ' ', datal['results'][keys]['uid'])
		order_id = datal['results'][keys]['order_id']
		for y in datal['results'][keys]['barcodes']:
			parcelNums = y
			print('BARCODE = ', y)
		# conn_2 = http.client.HTTPSConnection("api.pulse.express")
		# q = "/v1/parcels/" + datal['results'][keys]['uid'] + "/events/"
		conn_2.request("GET", "/v1/parcels/" + datal['results'][keys]['uid'] + "/events/", headers=headers)
		# print(q)
		reas = conn_2.getresponse()
		dataz = reas.read()
		# L = reas.read()
		L = json.loads(dataz.decode("utf-8"))
		# print(L)
		z = 0
		issued_time = None
		issued_date = None
		delivered_time = None
		delivered_date = None
		delivering_time = None
		delivering_date = None
		for x in L:
			# print(x)
			# print(L[z]['data']['status'], '- status')
			time_edit = L[z]['datetime']
			T_time = time_edit.find('T')
			dot_time = time_edit.find('.')
			# print(L[z]['datetime'][:T_time], 'date')
			# print(L[z]['datetime'][T_time+1:dot_time], 'time')
			try:
				if L[z]['data']['status'] == 'Выдана':
					print('посыль выдана ', L[z]['datetime'][:T_time], ' В ', L[z]['datetime'][T_time + 1:dot_time])
					issued_time = L[z]['datetime'][T_time + 1:dot_time]
					issued_date = L[z]['datetime'][:T_time]
				if L[z]['data']['status'] == 'Доставлена':
					print('посыль доставлена ', L[z]['datetime'][:T_time], ' В ', L[z]['datetime'][T_time + 1:dot_time])
					delivered_time = L[z]['datetime'][T_time + 1:dot_time]
					delivered_date = L[z]['datetime'][:T_time]
				if L[z]['data']['status'] == 'В доставке':
					print('посыль в доставке ', L[z]['datetime'][:T_time], ' В ', L[z]['datetime'][T_time + 1:dot_time])
					delivering_time = L[z]['datetime'][T_time + 1:dot_time]
					delivering_date = L[z]['datetime'][:T_time]
			except:
				print('succes')
			
			z += 1
		ref = 'https://internal.pulse.express/parcels/' + datal['results'][keys]['uid']
		add_dop(issued_time, issued_date, delivered_time, delivered_date, delivering_time, delivering_date, order_id,
		        parcelNums, ref)
		# print('da')
		keys += 1
	# time.sleep(2)


# print(datal['results'])
# print(data.decode("utf-8"))
def add_dop(issued_time, issued_date, delivered_time, delivered_date, delivering_time, delivering_date, order_id,
            parcelNum, ref):
	puth = 'consignors_temp_' + str(get_time(True)) + 'json'
	puth_dumps = 'consignors_dumps_temp_' + str(get_time(True)) + '.json'
	data_dop = load_file_d()
	if issued_time == None:
		issued_time = ' '
		issued_date = ' '
	if delivered_time == None:
		delivered_time = ' '
		delivered_date = ' '
	if delivering_time == None:
		delivering_time = ' '
		delivering_date = ' '
	print('issued_time = ', issued_time, ' issued_date = ', issued_date, ' delivered_time = ', delivered_time,
	      'delivered_date = ', delivered_date, ' delivering_time = ', delivering_time, ' delivering_date = ',
	      delivering_date, ' order_id = ', order_id)
	counts = data_dop['count']
	i = 1
	while i < counts + 1:
		if ((data_dop[str(i)]['dpd_order'] == order_id) and (data_dop[str(i)]['parcelNum:'] == parcelNum)):
			data_dop[str(i)].update([('issued_time', issued_time)])
			data_dop[str(i)].update([('issued_date', issued_date)])
			data_dop[str(i)].update([('delivered_time', delivered_time)])
			data_dop[str(i)].update([('delivered_date', delivered_date)])
			data_dop[str(i)].update([('delivering_time', delivering_time)])
			data_dop[str(i)].update([('delivering_date', delivering_date)])
			data_dop[str(i)].update([('Date', delivering_date)])
			data_dop[str(i)].update([('ref', ref)])
		i += 1
	with open(puth, 'w') as fileq:
		json.dump(data_dop, fileq, ensure_ascii=False)
		fileq.close()
	with open(puth_dumps, 'w') as fileq:
		json.dump(data_dop, fileq, ensure_ascii=False)
		fileq.close()
