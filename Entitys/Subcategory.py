from Entitys.Category import Category


class Subcategory:
    def __init__(self,req):
        self.id=req['idSubcategory']
        self.name=req['name']
        self.category= Category(req['category'])