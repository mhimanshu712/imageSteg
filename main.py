import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

lis = []

for i in range(7,-1,-1):
    res = b'\x01'[0]<<i
    lis.append(res)


def write_img(img,msg):
    s_len = len(msg)
    f_string = '^START:' + str(s_len)+ ':' + msg
    str_len = len(f_string)
    sa,sb,sc = img.shape
    cchar, cbit = 0,0
    
    for c in range(sc):
        for b in range(sb):
            for a in range(sa):
                if cchar < str_len:
                    s = f_string[cchar]
                    i = lis[cbit]
                    
                    if ord(s) & i == 0:
                        # Check if the first bit is not zero
                        if img[a][b][c]%2 != 0:
                            img[a][b][c] -= 1
                    else:
                        #check if first bit is not one
                        if img[a][b][c]%2 == 0:
                            img[a][b][c] += 1
                            
                    if cbit == 7:
                        cbit = 0
                        cchar += 1
                    else:
                        cbit += 1
                        
                else:
                    return
                

def read_imgn(img,sa,sb,sc,n):
    str = []
    cn = 0
    n = n*8
    ea,eb,ec = img.shape
    ch = 0
    
    for c in range(ec):
        for b in range(eb):
            for a in range(ea):
                if cn < n:
                    num = img[a][b][c]
                    if num%2 != 0:
                        ch += lis[cn%8]
                    if cn%8 == 7:
                        str.append(chr(ch))
                        ch = 0
                    cn += 1
                else:
                    return ''.join(str)
                
    return ''.join(str)

def read_img(img):
    # Check if our tag is present
    res = read_imgn(img,0,0,0,7)
    if res != "^START:":
        print("No Message Here!  ",res)
        return ""
    
    #Read number of chars
    a,b,c = 8*7,0,0
    dig = []
    flag = 0
    for i in range(100):
        if flag == 1:
            break
        ch = 0
        for j in lis:
            num = img[a][b][c]
            if num%2 != 0:
                ch += j
            a += 1
        if ch == ord(':'):
            flag = 1
            break
        else:
            dig.append(chr(ch))
            
    
    # read message
    diglen = len(dig)
    dig = int(''.join(dig))
    print('Total chars: ',dig)
    res = read_imgn(img,0,0,0,dig+8+diglen)
    return res[8+diglen:]