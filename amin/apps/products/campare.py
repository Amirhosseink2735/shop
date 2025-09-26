class CampareProduct:
    def __init__(self,request):
        self.session=request.session
        campare_product=self.session.get("campare_product")
        if not campare_product:
            campare_product=self.session["campare_product"]=[]
        self.campare_product=campare_product
        self.count=len(self.campare_product)
        
        
    def __iter__(self):
        campare_product=self.campare_product.copy()
        for item in campare_product:
            yield item
            
            
    def add_to_campare_product(self,productId):
        productId=int(productId)
        if productId not in self.campare_product:
            self.campare_product.append(productId)
            self.count=len(self.campare_product)
            self.session.modified=True
            
            
    def delete_from_campare_product(self,productId):
        self.campare_product.remove(int(productId))
        self.session.modified=True
        
        
    def clear_campare_product(self):
        del self.session["campare_product"]
        self.session.modified=True
        
        
      