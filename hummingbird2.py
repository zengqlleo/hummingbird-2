from bitstream import BitStream
from numpy import *
import sys
s1=[7,12,14,9,2,1,5,15,11,6,13,0,4,8,10,3]
s2=[4,10,1,6,8,15,7,12,3,0,14,13,5,9,11,2]
s3=[2,15,12,1,5,6,10,13,14,8,3,4,0,11,9,7]
s4=[15,4,5,8,9,7,2,1,10,3,0,14,6,12,13,11]
def sbox(x):
    a1=x%16
    a2=(x/16)%16
    a3=(x/256)%16
    a4=x/4096
    return s1[a4]*4096+s2[a3]*256+s3[a2]*16+s4[a1]

def LeftRotation(x,bits):
    stream=BitStream()
    stream.write(x,uint16)
    x=stream.read(bool,bits)
    stream.write(x,bool)
    return stream.read(uint16)

def L(x):
    return x^LeftRotation(x,6)^LeftRotation(x,10)

def f(x):
    return L(sbox(x))

def WD16(x,a,b,c,d):
    return f(f(f(f(x^a)^b)^c)^d)


def Initialization(K,R):

    for i in range(0,4):
        t1=WD16((R[0]+i)%65536,K[0],K[1],K[2],K[3])
        t2=WD16((R[1]+t1)%65536,K[4],K[5],K[6],K[7])
        t3 = WD16((R[2]+t2)%65536, K[0], K[1], K[2], K[3])
        t4 = WD16((R[3] + t3) % 65536, K[4], K[5], K[6], K[7])
        R[0]=LeftRotation((R[0]+t4)%65536,3)
        R[1]=LeftRotation((R[1]+t1)%65536,15)
        R[2]=LeftRotation((R[2]+t2)%65536,8)
        R[3]=LeftRotation((R[3]+t3)%65536,1)
        R[4]=R[4]^R[0]
        R[5]=R[5]^R[1]
        R[6]=R[6]^R[2]
        R[7]=R[7]^R[3]
    return

def Encryption(K,R,P):
    for i in range(0,8):
        t1=WD16(R[0]+P[i],K[0],K[1],K[2],K[3])
        t2=WD16((R[1]+t1)%65536,K[4]^R[4],K[5]^R[5],K[6]^R[6],K[7]^R[7])
        t3 = WD16((R[2] + t2) % 65536,K[0]^R[4],K[1]^R[5],K[2]^R[6],K[3]^R[7])
        C[i] = (WD16((R[3] + t3) % 65536, K[4], K[5], K[6], K[7])+R[0])%65536
        R[7]=R[7]^((R[3]+R[0]+t3+t1)%65536)
        R[6]=R[6]^((R[2]+t2)%65536)
        R[5]=R[5]^((R[1]+t1)%65536)
        R[4]=R[4]^((R[0]+t3)%65536)
        R[3]=(R[3]+R[0]+t3+t1)%65536
        R[2]=(R[2]+t2)%65536
        R[1]=(R[1]+t1)%65536
        R[0]=(R[0]+t3)%65536
        #print hex(C[i])
    return


IV=[0,0,0,0]
R=[IV[0],IV[1],IV[2],IV[3],IV[0],IV[1],IV[2],IV[3]]
K=[0,0,0,0,0,0,0,0]
P=[0,0,0,0,0,0,0,0]
C=[0,0,0,0,0,0,0,0]
Initialization(K,R)
Encryption(K,R,P)
for item in C:
    item=item/256+(item%256)*256

print C
bs=''
for item in C:
    bs = bs +str(hex(item))[2:-1].rjust(4,'0')
print bs

binfile = open('out.bin','wb')
binfile.write(bytes.fromhex(bs))
binfile.close()
