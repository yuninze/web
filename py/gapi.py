from os.path import exists
from time import time as t
from util import print_elapsed_time
from sl_lin import captivate,prep
import gspread
import pandas_gbq as from_gbq
import pydata_google_auth

test=input(f"sure?")

pat="c:/code"
cred=f"{pat}/gapi_oauth_cert.json"
cred_username=f"{pat}/gapi_ouath_cert_user.json"
proj_id="918911903550"
SCOPES=[
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/drive",]

def gs():
    if exists(f"{pat}/docid.txt"):
        with open(f"{pat}/docid.txt",encoding="utf-8") as idfile:
            docid=idfile.readline()
    else:
        docid=None
    if len(test)>1:
        #get test api auth
        t0=t()
        #gc=gspread.service_account(filename="c:/code/ga_ouath_cert.json")
        gapi_gs=gspread.oauth(
            credentials_filename=cred,
            authorized_user_filename=cred_username)
        print(f"got ouath cert")
        print_elapsed_time(t0)
        #get gsheet object
        t0=t()
        if not docid is None:
            #get test gs object
            gapi_gs_sheet=gapi_gs.open_by_key(docid)
        else:
            #create test gs object
            gapi_gs_sheet=gapi_gs.create("ext_gspread")
            #sh.share("ga",perm_type="user",role="writer")
            #have docid file as we created new docid
            docid=gapi_gs_sheet.id
            with open(f"{pat}/docid.txt","w",encoding="utf-8") as idfile:
                idfile.writelines([docid])
            print(f"docid file has been written")
        try:
            gapi_gs_sheet_worksheet=(
                gapi_gs_sheet.add_worksheet(
                    title="data",rows=2000,cols=20))
        except:
            #get worksheet cursor by index
            gapi_gs_sheet_worksheet=gapi_gs_sheet.get_worksheet("data")
        finally:
            print(f"got worksheet")
            print_elapsed_time(t0)
        #clear worksheet
        gapi_gs_sheet_worksheet.clear()
        #have things
        t0=t()
        #get test data object
        data=prep(captivate())
        #csv style per-row inputting
        (gapi_gs_sheet_worksheet
            .update(
                [data.columns.tolist()]+data.values.tolist()))
        print(f"updated")
        print_elapsed_time(t0)

def gbq():
    #using pydata_google_auth does not require ouath2 json
    cred=pydata_google_auth.get_user_credentials(
        scopes=SCOPES,
        auth_local_webserver=True)
    from_gbq.read_gbq("select * from tbl0",
    project_id=proj_id,
    credentials=cred)

#https://pandas-gbq.readthedocs.io/en/latest/writing.html