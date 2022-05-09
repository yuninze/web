from time import time as t
from util import print_elapsed_time
import gspread
import sl_lin

test=input(f"sure?")
pat="c:/code"

if str(len(test))>1:

    #get test api auth
    t0=t()
    #gc=gspread.service_account(filename="c:/code/ga_ouath_cert.json")
    gapi_gs=gspread.oauth(
        credentials_filename=f"{pat}/gapi_oauth_cert.json",
        authorized_user_filename=f"{pat}/gapi_ouath_cert_user.json")
    print(f"got ouath cert")
    print_elapsed_time(t0)

    #get gsheet object
    t0=t()
    try:
        #create test gs object
        gapi_gs_sheet=gapi_gs.create("test")
        #share to someone
        #sh.share("ga",perm_type="user",role="writer")
    except:
        #get test gs object
        gapi_gs_sheet=gapi_gs.open("test")
    #get worksheet cursor by index
    gapi_gs_sheet_worksheet=gapi_gs_sheet.get_worksheet(0)
    print(f"got worksheet")
    print_elapsed_time(t0)

    #clear worksheet
    gapi_gs_sheet_worksheet.clear()

    #have things
    t0=t()
    #get test data object
    data=sl_lin.prep(sl_lin.captivate())
    #csv style per-row inputting
    (gapi_gs_sheet_worksheet
        .update(
            [data.columns.tolist()]+data.values.tolist()))
    print_elapsed_time(t0)

raise Exception("quitted")