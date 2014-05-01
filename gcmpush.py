from gcmclient import *
#our API KEY is AIzaSyAMi6Rn-f-PNcDTQckbtb_nR88BRJb71p0
API_KEY = "AIzaSyBgwklrw5nMnsFXdFTIpBT0VsSl72OjOAE"
gcm = GCM(API_KEY)

def send_gcm_msg(dids, msg):
	#dids comes in a format [[["device id"], ["emailaddress"]],[["device id"], ["emailaddress"]]]
	#so grab every other device id starting at 0
	deviceids = []
	#after this loop deviceids is ["regid1", "regid2"] format
	#ready to hand to multicast
	for info in dids:
		for i in range(0, len(info), 2):
		   deviceids.append(info[i][0])


	
	#construct our key=>message payload, do not use nested structures.
	data = {'msg': msg, 'int': 10 }
	unicast = PlainTextMessage(dids[0], data, dry_run=False)
	multicast = JSONMessage(deviceids, data, collapse_key='my.key', dry_run=False)

	try:
		#attempt send
		res_unicast = gcm.send(unicast)
		res_multicast = gcm.send(multicast)
		#res_multicast = gcm.send(multicast)
		#for res in [res_unicast, res_multicast]:
		for res in [res_unicast, res_multicast]:
			#nothing to do on success
			for reg_id, msg_id in res.success.items():
				print "Successfully sent %s as %s" % (reg_id, msg_id)

			#update your registration ID's
			for reg_id, new_reg_id in res.canonical_items():
				print "Replacing %s with %s in id list" % (reg_id, new_reg_id)

			#probably app uninstalled
			for reg_id in res.not_registered:
				print "Removing %s from id list" % reg_id

			#unrecoverably failed, these ID's will not be retried
			for reg_id, err_code in res.failed.items():
				print "Removing %s because %s" % (reg_id, err_code)

			#if some reg ids have recoverably failed
			#for res.needs_retry():
				#construct new message with only failed regids
				#retry_msg = res.retry()
				#you have to wait before attempting again. delay()
				#will tell you how long to wait depending on your
				#current retry counter, starting from 0.
				#print "Wait or schedule task after %s seconds" % res.delay(retry)
				#retry += 1 and send retry_msg again

	except GCMAuthenticationError:
		# stop and fix your settings
		print "Your Google API key is rejected"
	except ValueError, e:
		#probably your extra options are invalid read error for more info.
		print "Invalid message/option or invalid GCM response"
	except Exception:
		#your network is down or proxy settings broken. retry when fixed
		print "Something wrong with requests library"
