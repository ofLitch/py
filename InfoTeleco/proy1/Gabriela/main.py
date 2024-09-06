import rsa
import pickle

# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
# key length should be at least 16
#--------------------- Client keys
private_key, public_key = rsa.newkeys(512)

file_pri = open('pri_key_client.txt', 'wb')
pickle.dump(private_key, file_pri)
file_pri.close()

file_pub = open('pub_key_client.txt', 'wb')
pickle.dump(public_key, file_pub)
file_pub.close()

private_key2, public_key2 = rsa.newkeys(512)

file_pri2 = open('pri_key_client2.txt', 'wb')
pickle.dump(private_key2, file_pri2)
file_pri2.close()

file_pub2 = open('pub_key_client2.txt', 'wb')
pickle.dump(public_key2, file_pub2)
file_pub2.close()