class Sale:
    def __init__(self,req):
        self.id=req['ventasId']
        self.client=req['cliente']
        self.total=req['total']
        self.payment=req['metodo_pago']