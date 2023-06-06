#This app is crudely mimicing a "malicious" or "altered" IoT binary. 

#The program is very small, and the CNN model was having trouble realizing it is an alternate program
#importing the library helps it realize it is different from the original memory

#This would not be an issue in the case of a real malware infection, since most malware code is substantial

import mfrc522

# Function to convert decimal number
# to binary using recursion
def DecimalToBinary(num):

    if num >= 1:
        DecimalToBinary(num // 2)
    print(num % 2, end = '')
 
# Driver Code
num=0
while(1):

    # decimal value
    dec_val = num

    # Calling function
    DecimalToBinary(dec_val)
    num = num + 1
