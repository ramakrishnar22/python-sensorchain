from hashlib import sha256
import json
import time
from urllib.parse import urlparse
import os,ast
from flask import  Blueprint,render_template,request,Response
import base64
from Crypto.Cipher import AES

class Block:
    def __init__(self,data,prev=0,index=0):
        self.index=index
        self.timestamp=time.ctime(time.time())
        self.data=data
        self.prevhash=prev
        self.nonce=0
    def __eq__(self,other):
        return self.__dict__ == other.__dict__

class Blockchain:
    
    def __init__(self):
        self.chain=[]
        self.create_genesis_block()

    def proof_of_work(self,block):
        block.nonce=0
        cdata,cprevhash,cnonce=block.data,block.prevhash,block.nonce
        comp=self.compute_hash(cdata,cprevhash,cnonce)
        stime=time.time()
        while not comp.startswith("0"*2) :
            cnonce+=1
            comp=self.compute_hash(cdata,cprevhash,cnonce)
        etime=time.time()
        s=time.localtime(stime).tm_min
        e=time.localtime(etime).tm_min
        d=e-s
        if d<=10:
            block.hash,block.nonce=comp,cnonce
            return True
        else:
            return False
    def compute_hash(self,data,prevhash,nonce):
        blockstr=(str(data)+str(prevhash)+str(nonce)).encode()
        return sha256(blockstr).hexdigest()

    def create_genesis_block(self):
         block=Block( {
           "Temperature":"0",
           "Humidity":"0"
        })
         block.hash=self.compute_hash(block.data,block.prevhash,block.nonce)
         self.chain.append(block)

    def add_new_block(self,block):
        block.index=len(self.chain)
        prevblock=self.chain[-1]
        phash=prevblock.hash
        block.prevhash=phash
        b=self.proof_of_work(block)
        if b:
            self.chain.append(block)
            return True
        else:
            cd.append(block.__dict__)
            return False
    def validate_block(self,block):
        chash,cdata,cphash,cnonce=block.hash,block.data,block.prevhash,block.nonce
        comp=self.compute_hash(cdata,cphash,cnonce)
        return comp==chash
    def displaydata(self):
        dval=self.chain
        c=[]
        for ddata in reversed(dval):
            c.append(ddata.__dict__)
        return json.dumps(c,separators=(',',':'))
    def mine(self,obj):
        no=int(obj['index'])
        h=obj['hash']
        d=obj['data']
        cchain=self.chain[:no]
        ccchain=self.chain[no:]
        # Copy the partial blocks before hand for the proof of work to perform 
        prev=cchain[-1]
        if not self.comp_data(ccchain[0].data,d):
            for k in ccchain:
                block=Block("")
                if h==k.hash and k.index==no:
                    block.data=d
                    block.index=k.index
                    block.prevhash=prev.hash
                else:
                    block.prevhash=cchain[-1].hash
                    block.index=len(cchain)
                    block.data=k.data
                q=self.proof_of_work(block)
                if q:
                    cchain.append(block)
                else:
                    cd.append(block.__dict__)
            self.chain=cchain
            return True
        else:
             return False
    def comp_data(self,obj1,obj2):
        print(obj1,obj2)
        print(obj1==obj2)
        return obj1==obj2
        

# Starting line of the code  
cd=[]
bd=Blueprint('blockdata',__name__)
bb=Blockchain()

# Create routes for the backend
@bd.route("/")
def index():
    return render_template('home.html')
# API router for home html
@bd.route("/display")
def dis():
    return bb.displaydata()


@bd.route("/valid/<int:i>")
def valid(i):
    print(len(bb.chain))
    if i==1:
        return "Enter value greater than 1"
    if 1<= i-1 <len(bb.chain) and bb.validate_block(bb.chain[i-1]):
        return "Yes it is"
    elif not (i<= i-1 <len(bb.chain)):
        return "No it is not in range"
    elif not (bb.validate_block(bb.chain[i-1])):
        return "Not validated"
    else:
        pass
# Dynamic adding of data from the script to the server
@bd.route("/add",methods=['POST'])
def addb():
    print("Received from client->{}".format(request.is_json))
    hexa=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    key="mypasswordisramsmypasswordisrams"
    print(request.get_data(as_text=True))
    w = request.get_data(as_text=True)
    gdec,giv=w['data'],w['iv']
    b64dec=base64.b64decode(gdec)
    print(b64dec)
    aes1=AES.new(key.encode('utf-8'),AES.MODE_CBC,giv.encode('utf-8'))
    d=aes1.decrypt(b64dec)
    f=d.decode('utf-8')
    print(f)
    trail=f[-1]
    v=0
    for ind,k in enumerate(hexa):
        if k == trail:
            v=ind
            break
    print(v)
    f=f[:-v]
    print(f)
    dis=ast.literal_eval(f)
    print(dis)
    cd.append(dis)
    return Response("Received successfully")
    # sw=bb.add_new_block(Block(q))
    # if sw == True:
    #     return Response("Received successfully")
    # else:
    #     return Response("Cannot added to the block")

# Shows the dynamically added data
@bd.route("/dd")
def dexceptdata():
    return json.dumps(cd)
# Shows the individual block details
@bd.route("/block")
def showsingleblock():
    return render_template('block.html')
# Shows the mining of the block
@bd.route("/mine",methods=['POST'])
def minedata():
    newdata=request.get_json(force=True)
    w=bb.mine(newdata)
    if w:
        return "Successfully added to the block"
    else:
        return "unsuccessful"