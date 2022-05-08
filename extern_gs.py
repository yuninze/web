from time import time as t
from util import print_elapsed_time
import gspread
import sl_lin

tst=input(f"sure?")
if tst:
    t0=t()
    #get test api auth
    #yiz-gspread@long-way-330412.iam.gserviceaccount.com
    gc=gspread.service_account(filename="gsak.json")
    print_elapsed_time(t0)

    t0=t()
    #sh=gc.create("test")
    #sh.share("@gamil.com",perm_type="user",role="writer")
    #get sheet "test"
    sht=gc.open("test")
    #get worksheet cursor by index
    sht=sht.get_worksheet(0)
    print_elapsed_time(t0)

    data=sl_lin.prep(sl_lin.captivate())

    t0=t()
    #per-row format like csv
    sht.update([data.columns.tolist()]+data.values.tolist())
    print_elapsed_time(t0)

raise Exception("quitted")