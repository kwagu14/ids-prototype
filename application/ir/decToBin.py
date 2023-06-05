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
