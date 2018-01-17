

class Category():
    curr_id = 0
    def __init__(self, name, limit, spent,cat_id=None):
        if cat_id is None:
            self.cat_id = Category.curr_id
            Category.curr_id = Category.curr_id+1
        else:
            self.cat_id= cat_id
        self.limit = limit
        self.spent=spent
        self.name= name
        
        
    
class Purchase():
    default_cat_id = -1 
    curr_id = 0
    
    def __init__(self, amount, spentOn, date,cat_id=None):
        self.p_id= Purchase.curr_id+1
        Purchase.curr_id = Purchase.curr_id+1
        if cat_id is None:
            self.cat_id= Purchase.default_cat_id
        else:
            self.cat_id = cat_id
        self.amount = amount
        self.spentOn = spentOn
        self.date = date
        
        
        
        