import http.client
import datetime
import json
import time

def get_secur(param):
	puth = 'conf.conf'
	f = open(puth)
	securs = f.read()
	f.close()
	partnerCode_num = securs.find('partnerCode')
	clientKey_num = securs.find('clientKey')
	authorization_num = securs.find('authorization')
	partnerCode = securs[partnerCode_num + 14:clientKey_num-1]
	clientKey = securs[clientKey_num+12:authorization_num -1]
	authorization = securs[authorization_num+16:]
	print(partnerCode)
	print(clientKey)
	print(authorization)
	if param == "pc": return partnerCode
	if param == "ck": return clientKey
	if param == "au": return authorization  


def get_information(payload):
	conn = http.client.HTTPConnection("ws.dpd.ru:80")
	headers = {
		'content-type': "text/xml",
		'cache-control': "no-cache"
		}
	try:
		conn.request("POST", "/services/partnership?wsdl=", payload, headers)
		res = conn.getresponse()
		print(res)
	except:
		conn.request("POST", "/services/partnership?wsdl=", payload, headers)
		res = conn.getresponse()
		print(res)
	#res = requests.post('/services/partnership?wsdl=', payload, headers)
	data = res.read()
	redata = data.decode("utf-8")
	#print(redata)
	conn.close()
	return redata

def get_time(param):
	now = datetime.datetime.now()
	str_time = str(now.strftime('%Y-%m-%d'))
	str_date = str(now.strftime('%H:%M:%S'))
	if param:
		return str_time
	else:
		return str_date

def find_strings(data):
	beg = data.find('<return>')
	end = data.find('</return>')
	if beg != -1:
		station_n_begin = data.find('<stationNum>')
		station_n_end = data.find('</stationNum>')
		pointCode_beg = data.find('<pointCode>')
		pointCode_end = data.find('</pointCode>')
		print(data[station_n_begin + 12: station_n_end])
		print('Pochtomat #', data[pointCode_beg + 11: pointCode_end])
		payload_beg = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://dpd.ru/ws/partnership/2015-03-20\">\n   <soapenv:Header/>\n   <soapenv:Body>\n      <ns:getOrderListDelivery>\n         <!--Optional:-->\n         <request>\n            <auth>\n               <partnerCode>'+ get_secur('pc') + '</partnerCode>\n               <clientKey>' + get_secur('ck') + '</clientKey>\n            </auth>\n            <stationNum>'
		payload_cent = data[station_n_begin + 12: station_n_end]
		payload_end = '</stationNum>\n         </request>\n      </ns:getOrderListDelivery>\n   </soapenv:Body>\n</soapenv:Envelope>'
		payload_all = payload_beg + payload_cent + payload_end
		#time.sleep(15)
		find_consignor(get_information(payload_all),data[station_n_begin + 12: station_n_end],data[pointCode_beg + 11: pointCode_end])
		try:
			find_strings(data[end + 9:])
		except:
			time.sleep(10)
			find_strings(data[end + 9:])



def find_consignor(data, stationNums, pointCode):
	beg = data.find('<order>')
	end = data.find('</order>')
	if beg != -1:
		dpdOrderNum = data.find('<dpdOrderNum>')
		dpdOrderNum_e = data.find('</dpdOrderNum>')
		parcelNum = data.find('<parcelNum>')
		parcelNum_e = data.find('</parcelNum>')
		consignor = data.find('<consignor>')
		consignor_e = data.find('</consignor>')
		#value_dpdOrderNum = {}
		value_parcelNum = {}
		value_consignor = {}
		value = {}
		if dpdOrderNum != -1:
			value_dpdOrderNum = data[dpdOrderNum+13:dpdOrderNum_e]
			print('dpdOrderNum = ', value_dpdOrderNum)
			value_header = {value_dpdOrderNum: {}}
			if parcelNum != -1:
				print('parcelNum = ', data[parcelNum+11:parcelNum_e])
				ParcelNum = data[parcelNum+11:parcelNum_e]
				if consignor != -1:
					print('consignor = ', data[consignor+11:consignor_e])
					consignors = data[consignor+11:consignor_e]
			value = {
			'dpd_order': value_dpdOrderNum,
			'parcelNum:': ParcelNum, 
			'Time': get_time(False), 
			'stationNums': stationNums,
			'Date': get_time(True),
			'pointCode': pointCode,
			'consignor': consignors
				}
		#value_header.update([(value_dpdOrderNum, value)])
		#save_in(value_dpdOrderNum, value)
		save_in(value)
		print(value_header)
		#print(data[beg:end + 8])
		find_consignor(data[end+8:], stationNums, pointCode)

def load_file_d():
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
			paxa = {}
			with open(puth, 'w') as fiiil:
				json.dump(paxa, fiiil, ensure_ascii=False)
			fiiil.close()
			return paxa
def save_in(value):
	puth = 'consignors.json'
	puth_dumps = 'consignors_dumps.json'
	last_file = load_file_d()
	counts = last_file['count']
	i = 1
	flag = True
	while ((i<counts+1) and (flag == True)):
		if ((last_file[str(i)]['dpd_order'] == value['dpd_order']) and (last_file[str(i)]['parcelNum:'] == value['parcelNum:'])):
			flag = False
		i +=1
	if flag == True:
		last_file.update([('count', counts + 1)])
		last_file.update([(counts + 1, value)])
		with open(puth, 'w') as fileq:
			json.dump(last_file, fileq, ensure_ascii=False)
			fileq.close()
		with open(puth_dumps, 'w') as filet:
			json.dump(last_file, filet, ensure_ascii=False)
			filet.close()



def get_parcel_pulse():
	conn = http.client.HTTPSConnection("api.pulse.express")
	conn_2 = http.client.HTTPSConnection("api.pulse.express")
	headers = {
	'content-type': "application/json",
	'authorization': ""
	}

	conn.request("GET", "/v1/parcels/?limit=1500", headers=headers)

	res = conn.getresponse()
	data = res.read()
	conn.close()
	datal = json.loads(data.decode("utf-8"))
	keys = 0
	while keys< 1500:
		parcelNums = None
		print(datal['results'][keys]['order_id'], ' ', datal['results'][keys]['uid'])
		order_id = datal['results'][keys]['order_id']
		for y in datal['results'][keys]['barcodes']:
			parcelNums = y
			print('BARCODE = ', y)
		#conn_2 = http.client.HTTPSConnection("api.pulse.express")
		#q = "/v1/parcels/" + datal['results'][keys]['uid'] + "/events/"
		conn_2.request("GET", "/v1/parcels/" + datal['results'][keys]['uid'] + "/events/", headers=headers)
		#print(q)
		reas = conn_2.getresponse()
		dataz = reas.read()
		#L = reas.read()
		L = json.loads(dataz.decode("utf-8"))
		#print(L)
		z = 0
		issued_time = None
		issued_date = None
		delivered_time = None
		delivered_date = None
		delivering_time = None
		delivering_date = None
		for x in L:
			#print(x)
			#print(L[z]['data']['status'], '- status')
			time_edit = L[z]['datetime']
			T_time = time_edit.find('T')
			dot_time = time_edit.find('.')
			#print(L[z]['datetime'][:T_time], 'date')
			#print(L[z]['datetime'][T_time+1:dot_time], 'time')
			try:
				if L[z]['data']['status'] == 'Выдана':
					print('посыль выдана ', L[z]['datetime'][:T_time], ' В ', L[z]['datetime'][T_time+1:dot_time])
					issued_time = L[z]['datetime'][T_time+1:dot_time]
					issued_date = L[z]['datetime'][:T_time]
				if L[z]['data']['status'] == 'Доставлена':
					print('посыль доставлена ', L[z]['datetime'][:T_time], ' В ', L[z]['datetime'][T_time+1:dot_time])
					delivered_time = L[z]['datetime'][T_time+1:dot_time]
					delivered_date = L[z]['datetime'][:T_time]
				if L[z]['data']['status'] == 'В доставке':
					print('посыль в доставке ', L[z]['datetime'][:T_time], ' В ', L[z]['datetime'][T_time+1:dot_time])
					delivering_time = L[z]['datetime'][T_time+1:dot_time]		
					delivering_date = L[z]['datetime'][:T_time]
			except:
				print('succes')	

			z += 1
		ref = 'https://internal.pulse.express/parcels/'+ datal['results'][keys]['uid']
		add_dop(issued_time, issued_date, delivered_time, delivered_date, delivering_time, delivering_date, order_id, parcelNums, ref)
		#print('da')
		keys += 1
		#time.sleep(2)
	#print(datal['results'])
	#print(data.decode("utf-8"))
def add_dop(issued_time, issued_date, delivered_time, delivered_date, delivering_time, delivering_date, order_id, parcelNum, ref):
	puth = 'consignors.json'
	puth_dumps = 'consignors_dumps.json'
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
	print('issued_time = ', issued_time, ' issued_date = ', issued_date, ' delivered_time = ', delivered_time, 'delivered_date = ',delivered_date, ' delivering_time = ', delivering_time, ' delivering_date = ', delivering_date, ' order_id = ', order_id)
	counts = data_dop['count']
	i = 1
	while i<counts+1:
		if ((data_dop[str(i)]['dpd_order'] == order_id) and (data_dop[str(i)]['parcelNum:'] == parcelNum)):
			data_dop[str(i)].update([('issued_time', issued_time)])
			data_dop[str(i)].update([('issued_date', issued_date)])
			data_dop[str(i)].update([('delivered_time', delivered_time)])
			data_dop[str(i)].update([('delivered_date', delivered_date)])
			data_dop[str(i)].update([('delivering_time', delivering_time)])
			data_dop[str(i)].update([('delivering_date', delivering_date)])
			data_dop[str(i)].update([('Date', delivering_date)])
			data_dop[str(i)].update([('ref', ref)])
		i +=1
	with open(puth, 'w') as fileq:
		json.dump(data_dop, fileq, ensure_ascii=False)
		fileq.close()
	with open(puth_dumps, 'w') as fileq:
		json.dump(data_dop, fileq, ensure_ascii=False)
		fileq.close()

if __name__=='__main__':
	payload = "<?xml version='1.0' encoding='UTF-8'?>\n\n\t<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://dpd.ru/ws/partnership/2015-03-20\">\n\t<soapenv:Header>\n\n    </soapenv:Header>\n   <soapenv:Body>\n      <ns:getPointList>\n        <auth>\n           <partnerCode>"+get_secur('pc') + " </partnerCode>\n           <clientKey>"+get_secur('ck')+"</clientKey>\n        </auth>\n      </ns:getPointList>\n      <return>\n\n      </return>\n   </soapenv:Body>\n</soapenv:Envelope>"
	find_strings(get_information(payload))
	#get_parcel_pulse()

