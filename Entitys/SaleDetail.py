from Entitys.Product import Product
from Entitys.Sale import Sale


class SaleDetail:
    def __init__(self,req):
        self.id=req['detailId']
        self.amount=req['cantidad']
        self.subtotal=req['subtotal']
        self.product=Product(req['product'])
        self.sale=Sale(req['sale'])