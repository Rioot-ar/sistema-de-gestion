from Entitys.Brand import Brand
from Entitys.Subcategory import Subcategory


class Product:
    def __init__(self,req):
        self.id=req['id_product']
        self.name=req['name']
        self.cost=req['cost']
        self.stock=req['stock']
        self.subcategory=Subcategory(req['subcategory'])
        self.brand=Brand(req['brand'])