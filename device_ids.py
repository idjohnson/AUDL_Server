id_list = []

def add_id(num, email):
	print num
	print email
	id_list.append([num, email])
	print id_list

def write_to_file():
	f = open('deviceids.txt' , 'w')
	for i in id_list:
		f.write(i[0] + " " + i[1] + "\n")
	f.close()

def read_from_file():
	f = open('deviceids.txt' , 'r')

