import string,random
import pandas as pd

def truthy(*vals):
    for x in vals:
        if not x:
            raise SystemExit(f"{x}")

def idgen()->str:
    return "".join(
        random.choices(
            string.ascii_uppercase,k=8))

class ed:
    def __init__(self,f,n,id):
        self.content=f
        self.name=n
        self.id=id
        self.des=f.describe()
    def zs(self):
        return self.content.describe()

setattr(ed,id,"id")