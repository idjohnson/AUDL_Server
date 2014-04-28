import urllib
import urllib2

url = 'http://localhost:4000'
post_dict = {'ID' : 185982529582123,
             'email' : "johnnieDoe@example.com" }

params = urllib.urlencode(post_dict)
post_req = urllib2.Request(url)
post_req.add_data(params)

response = urllib2.urlopen(post_req)
response_data = response.read()
response.close()
print response_data
