class Brand:
    def __init__(self,req):
        self.id=req['idBrand']
        self.name=req['name']