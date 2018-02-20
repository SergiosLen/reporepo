import gzip
import csv
# import boto3
import decimal as dc
import urllib.request, json 

# from collections import OrderedDict

class Product(object):
    """digest csv data to dictionary"""
    def __init__(self, arg):
        self.inData={}# OrderedDict()
        # if arg[]
        # self.arg=arg
        self.id=arg[0].strip()
        self.name=arg[1].strip().replace('"','')
        self.brand=arg[2].strip().replace('"','')
        self.retailer=arg[3].strip().replace('"','')
        try:
            price=dc.Decimal(arg[4])
        except:
            price =None
        self.price=price

        self.in_stock= arg[5].strip().replace('"','')
        self.inData['id']= self.id
        if len(self.name)>0:

            self.inData['name']=self.name
        else:
            self.inData['name']=None
        if len(self.brand)>0:
            self.inData['brand']=self.brand
        else:
            self.inData['brand']=None
        if len(self.retailer)>0:
            self.inData['retailer']=self.retailer
        else:
            self.inData['retailer']=None
        self.inData['price']=self.price
        if self.in_stock in ('y', 'yes',True):
            self.inData['in_stock']=True
        elif self.in_stock in ('n', 'no',False):
            self.inData['in_stock']=False
        else:
            self.inData['in_stock']=None

    def get_data(self):
        """return the id and a dictionary of all the keys values"""
        return self.id,self.inData

def parse_dict(dictionary):
    """ Transform dictionary from S3 to be comparable with the dictionary of csv data"""
    # print (dictionary.keys())
    if 'name' not in dictionary or not isinstance(dictionary['name'],str) or len(dictionary['name'])==0:
        dictionary['name']=None
    if 'brand' not in dictionary or  not isinstance(dictionary['brand'],str) or len(dictionary['brand'])==0:
        dictionary['brand']=None
    if 'retailer' not in dictionary or not isinstance(dictionary['retailer'],str) or len(dictionary['retailer'])==0:
        dictionary['retailer']=None
    try:
        price=dc.Decimal(dictionary['price'])
    except:
        dictionary['price']=None
    if 'in_stock'  in dictionary and  isinstance(dictionary['in_stock'],str) and dictionary['in_stock'] in ('n', 'no', False):
        dictionary['in_stock']=False
    elif 'in_stock'  in dictionary and  isinstance(dictionary['in_stock'],str) and dictionary['in_stock'] in ('y','yes',True):
        dictionary['in_stock']=True
    else:
        dictionary['in_stock']=None
    return dictionary



data={}
data_names=['id','name','brand','retailer','price','in_stock']

with urllib.request.urlopen("https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json") as url:
    data_S3 = json.loads(url.read().decode())
    for dat in data_S3:
        dat=parse_dict(dat)
        data[dat['id']]={}#OrderedDict()
        for name in data_names:
            data[dat['id']][name]=dat[name]
        # print (dat,type(dat))
    # print(data)
# print(len(data))
with gzip.open('products.csv.gz', 'rt') as fop:
    reader=csv.reader(fop)#,quotechar='"',quoting=csv.QUOTE_NONE)
    for lin in reader:
        if lin[0]=='Id':
            continue
        product_line=Product(lin)
        product_id,product_values=product_line.get_data()
        # print(product_id,product_values,lin)
        data[product_id]=product_values
# print (len(data))

