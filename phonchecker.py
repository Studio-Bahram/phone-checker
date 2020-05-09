from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.types import InputPhoneContact

import time
import json
import random

db_good = []

def msg(text:str,mode:int,color:str="\033[0;32m"):
    if mode == 1:
        txt = f"\033[0;36m[\033[0;32m$\033[0;36m] {color}{text} \033[0;34m\> \033[0m"
    elif mode == 31:
        txt = f"\033[0;31mError ==> {text} \033[0m"
    else:
        txt = f"\033[0;36m[\033[0;33m#\033[0;36m] {color}{text}\033[0m"
    return txt

def gets_from_user():
    try:
        api_id = input(msg("Enter id your account",1))
        if api_id.isnumeric():
            api_id = int(api_id)
        else:
            while True:
                api_id = input(msg("Enter id your account \033[0;31mOnly Number",1))
                if api_id.isnumeric():
                    api_id = int(api_id)
                    break
        api_hash = input(msg("Enter \033[0;35mHasH\033[0;32m Your Account",1))
        if len(api_hash) < 15:
            while True:
                api_hash = input(msg("Enter \033[0;35mHasH\033[0;32m Your Account",1))
                if len(api_hash) > 15:
                    break
        db_phones = input(msg("Enter Name your File \033[0;33mPhone Numbers",1))
        if db_phones == "":
            while True:
                db_phones = input(msg("Enter Name your File Phone Numbers \033[0;31m None :| ",1))
                if db_phones != "":
                    break
        if db_phones.find(".txt") == -1:
            db_phones = db_phones + ".txt"
        gfilename = input(msg("Enter Name for \033[0;35mSave \033[0;32mGooDs \033[0;33mPhone Number",1))
        if gfilename == "":
            gfilename = "THIS_GOOD_PHONE_NUMBERS"
        g = "\033[0;36m[\033[0;33m#\033[0;36m] "
        tt = "\033[0;36m"+("-" * 40)
        text = f"{tt}\n{g}\033[0;32mYour Account id \033[0;37m= \033[0;33m{api_id} \n{g}\033[0;32mYour account HasH \033[0;37m= \033[0;33m{api_hash} \n{g}\033[0;32mFile list Phone Numbers \033[0;37m= \033[0;33m{db_phones} \n{g}\033[0;32mFile Save  \033[0;37m= \033[0;33m{gfilename}.json\033[0m\n{tt}"
        print(text)
        verfie = input(msg("Send \033[0;33m[yes/y]\033[0;32m to confirm and \033[0;33m[q/Q] \033[0;32mto exit",1))
        if verfie == "yes" or verfie =="y":
            return {"api_id":api_id,"api_hash":api_hash,"db_phones":db_phones,"gfilename":gfilename}
        elif verfie == "q" or verfie =="Q":
            quit()
        else:
            while True:
                verfie = input(msg("Send \033[0;33m[yes/y]\033[0;32m to confirm and \033[0;33m[q/Q] \033[0;32mto exit",1))
                if verfie == "yes" or verfie == "y":
                    return {"api_id":api_id,"api_hash":api_hash,"db_phones":db_phones,"gfilename":gfilename}
                elif verfie == "q" or verfie == "Q":
                    quit()
    except Exception as err:
        print(f"\033[0;31m{err}\033[0m")
        quit()

def write_to_f(gfname,db):
    try:
        print(msg(f"GOODs \033[0;35m {len(db)}",2))
        with open(f"{gfname}.json","w") as jf:
            json.dump(db,jf)
        print(msg(f"Your File Name \033[0;33m{gfname}.json\033[0m",2))
    except Exception as err:
        print(f"\033[0;31m{err}\033[0m")
        quit()

def get_client(api_id,api_hash):
    try:
        return TelegramClient("anon", api_id, api_hash)
    except Exception as err:
        print(f"\033[0;31m{err}\033[0m")
        quit()

def open_db(nmfile):
    try:
        with open(nmfile,"r") as f:
            db = f.read().splitlines()
        if len(db) == 0:
            print(msg("Not Found Your Numbers",31))
        else:
            print(msg(f"Find \033[0;36m{len(db)} \033[0;32mPhone Numbers",2))
            return db
    except Exception as err:
        print(f"\033[0;31m{err}\033[0m")
        quit()

async def phone_checker(client,db):
    try:
        global db_good
        print(msg("Start Cracking ...",2))
        for number in db:
            if number[0] != "+":
                number = "+" + number
            cmo = InputPhoneContact(client_id=random.randrange(-2**63, 2**63),phone=str(number),first_name='This',last_name="& This")
            result = await client(ImportContactsRequest(contacts=[cmo]))
            result = result.__dict__
            if len(result["users"]) > 0:
                usr = result["users"][0]
                dcusr = {"user_id":usr.id,"user_username":usr.username,"user_phone":usr.phone}
                db_good.append(dcusr)
                result = await client(DeleteContactsRequest(id=[usr.username]))
    except Exception as err:
        print(f"\033[0;31m{err}\033[0m")
        quit()

def main():
    try:
        dget = gets_from_user()

        api_id = dget["api_id"]
        api_hash = dget["api_hash"]
        db_phones = dget["db_phones"]
        gfname = dget["gfilename"]

        dbph = open_db(db_phones)
        client = get_client(api_id,api_hash)
        client.start()
        client.loop.run_until_complete(phone_checker(client,dbph))
        write_to_f(gfname,db_good)
    except Exception as err:
        print(f"\033[0;31m{err}\033[0m")
        quit()

if __name__ == "__main__":
    main()