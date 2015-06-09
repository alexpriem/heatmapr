from array import array


alist=[17,33,65]
f=open("test.bin","wb")

data_array=array('L',alist)
data_array.tofile(f)
data_array=array('L',[1])
data_array.tofile(f)
data_array=array('L',[2])
data_array.tofile(f)
data_array=array('L',[3])
data_array.tofile(f)
data_array=array('L',[4])
data_array.tofile(f)

f.close()


f=open("test.bin",'rb')
d=array('L')
d.fromstring(f.read())
print d[0]
