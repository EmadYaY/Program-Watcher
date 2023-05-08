import sys
import os
import configparser
import random
import json
import time
import urllib.request
from colorama import Fore, Back
from discord_webhook import *
import sqlite3

# ------------------------------------COLORS----------------------------------------------#
BLACK = Fore.BLACK
RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

# ------------------------------------BASE - CONFIGS----------------------------------------------#

config = configparser.ConfigParser()
config.read('E:\[+] HUNTIG COURSE YASHAR\Watchers\Program Watcher\config.ini')

DISCORD_WEBHOOK = config['DISCORD']['WEBHOOK']
CHECK_HACKERONE = config['PLATFORMS']['HACKERONE']
CHECK_BUGCROWD = config['PLATFORMS']['BUGCROWD']
CHECK_INTIGRITI = config['PLATFORMS']['INTIGRITI']
CHECK_YESWEHACK = config['PLATFORMS']['YESWEHACK']
SEND_NOTIFICATION = config["PERFORMANCE"]["SEND_NOTIFICATION"]

# ------------------------------------TITLES - CONFIGS----------------------------------------------#

NEW_TARGET_TITLE = config["MESSAGE"]["NEW_TARGET_TITLE"]
SCOPE_UPDATE_TITLE = config["MESSAGE"]["SCOPE_UPDATE_TITLE"]
OUT_OF_SCOPE_UPDATE = config["MESSAGE"]["OUT_OF_SCOPE_UPDATE"]

# ------------------------------------DB - CONFIGS----------------------------------------------#

BASE_DB_PATH = config["DB"]["BASE_DB_PATH"]

# ------------------------------------PERFORMANCE - CONFIGS----------------------------------------------#

PRINTING = config["PERFORMANCE"]["PRINT"]

# ------------------------------------VARIABLES----------------------------------------------#

HACKERONE_URL = "https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/hackerone.json"
BUGCROWD_URL = "https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/bugcrowd.json"
INTIGRITI_URL = "https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/intigriti.json"
YESWEHACK_URL = "https://raw.githubusercontent.com/Osb0rn3/bugbounty-targets/main/programs/yeswehack.json"

# ------------------------------------GET INFORMATION FUNCTIONS----------------------------------------------#


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


def hackerone():
    dict_list = []
    target_information = {}
    with urllib.request.urlopen(HACKERONE_URL) as url:
        print(Back.WHITE + BLACK +
              "[+] Fetching -> HACKERONE <- DATA .... " + RESET + Back.RESET)
        data = json.load(url)

    for target in data:
        name = target["attributes"]["handle"]
        submit = target["attributes"]["submission_state"]
        allows_bounty_splitting = target["attributes"]["allows_bounty_splitting"]
        logo = target["attributes"]["profile_picture"]
        colour = "#1f1f1f"
        program_handle = target["attributes"]["handle"]
        target_information = {"platform": "HACKERONE", "name": name,
                              "submit": submit, "logo": logo, "color": colour, "program_url": "https://hackerone.com/" + program_handle, "in-scope": [], "out-of-scope": [], "allows_bounty_splitting": allows_bounty_splitting}
        for scope in target["relationships"]["structured_scopes"]["data"]:
            asset_type = scope["attributes"]["asset_type"]
            asset_identifier = scope["attributes"]["asset_identifier"]
            eligible_for_submission = scope["attributes"]["eligible_for_submission"]
            asset_type = scope["attributes"]["asset_type"]
            if eligible_for_submission == True:
                target_information["in-scope"].append(
                    str(asset_identifier).strip())
            else:
                target_information["out-of-scope"].append(asset_identifier)
        dict_list.append(target_information)
    if len(dict_list) > 1:
        print(Back.WHITE + BLACK +
              "[+] -> HACKERONE <- Data Parsing Is Done !!! " + RESET + Back.RESET)
    else:
        print(Back.WHITE + BLACK +
              "[-] -> HACKERONE <- Data Parsing Is Faild !!! " + RESET + Back.RESET)
    return dict_list


def bugcrowd():
    dict_list = []
    with urllib.request.urlopen(BUGCROWD_URL) as url:
        print(Back.WHITE + YELLOW +
              "[+] Fetching -> BUGCROWD <-  DATA .... " + RESET + Back.RESET)
        data = json.load(url)
    for target in data:
        name = target["code"]
        submit = target["can_submit_report"]
        logo = target["logo"]
        colour = target["colour"]
        program_code = target["code"]
        target_information = {"platform": "BUGCROWD", "name": name, "submit": submit,
                              "logo": logo, "color": colour, "program_url": "https://bugcrowd.com/" + program_code, "scopes": []}
        for scope in target["target_groups"]:
            for t in scope["targets"]:
                scope_uri = t["uri"]
                if scope_uri != None and scope_uri != "":
                    target_information["scopes"].append(scope_uri)
        dict_list.append(target_information)
    if len(dict_list) > 1:
        print(Back.WHITE + YELLOW +
              "[+] -> BUGCROWD <- Data Parsing Is Done !!! " + RESET + Back.RESET)
    else:
        print(Back.WHITE + YELLOW +
              "[-] -> BUGCROWD <- Data Parsing Is Faild !!! " + RESET + Back.RESET)
    return dict_list


def intigriti():
    dict_list = []
    target_information = {}
    with urllib.request.urlopen(INTIGRITI_URL) as url:
        print(Back.WHITE + BLUE +
              "[+] Fetching -> INTIGRITI <- DATA .... " + RESET + Back.RESET)
        data = json.load(url)

    for target in data:
        name = target["handle"]
        submit = target["companySustainable"]
        logo = target["logoId"]
        colour = "#0000ff"
        program_handle = target["handle"]
        program_company_handle = target["companyHandle"]
        target_information = {"platform": "INTIGRITI", "name": name, "submit": submit, "logo": "https://bff-public.intigriti.com/file/" + logo,
                              "color": colour, "program_url": "https://app.intigriti.com/programs/" + program_company_handle + "/" + program_handle, "scope": []}
        for scope in target["domains"]:
            target_information["scope"].append(scope["endpoint"])

        dict_list.append(target_information)

    if len(dict_list) > 1:
        print(Back.WHITE + BLUE +
              "[+] -> INTIGRITI <- Data Parsing Is Done !!! " + RESET + Back.RESET)
    else:
        print(Back.WHITE + BLUE +
              "[-] -> INTIGRITI <- Data Parsing Is Faild !!! " + RESET + Back.RESET)
    return dict_list


def yeswehack():

    dict_list = []
    target_information = {}

    with urllib.request.urlopen(YESWEHACK_URL) as url:
        print(Back.WHITE + RED +
              "[+] Fetching -> YESWEHACK <- DATA .... " + RESET + Back.RESET)
        data = json.load(url)

    for target in data:
        name = target["business_unit"]["slug"]
        submit = target["business_unit"]["already_activate_product"]
        logo = target["business_unit"]["logo"]["url"]
        program_slug = target["slug"]
        colour = "#FF0000"
        target_information = {"platform": "YESWEHACK", "name": name, "submit": submit,
                              "logo": logo, "color": colour, "program_url": "https://yeswehack.com/programs/" + program_slug, "scope": []}
        for scope in target["scopes"]:
            if scope["scope_type"] == "web-application":
                if scope["scope"] != None:
                    target_information["scope"].append(scope["scope"])

        dict_list.append(target_information)
    if len(dict_list) > 1:
        print(Back.WHITE + RED +
              "[+] -> YESWEHACK <- Data Parsing Is Done !!! " + RESET + Back.RESET)
    else:
        print(Back.WHITE + RED +
              "[-] -> YESWEHACK <- Data Parsing Is Faild !!! " + RESET + Back.RESET)
    return dict_list


# ------------------------------------ CHECK & DB FUNCTIONS ----------------------------------------------#
def db_exist():
    if not os.path.exists(BASE_DB_PATH):
        os.makedirs(BASE_DB_PATH)

    names = ["yeswehack", "intigriti", "bugcrowd", "hackerone"]
    for name in names:
        check = os.path.exists(f"{BASE_DB_PATH}{name}.db")
        if not check:
            print(Back.WHITE + RED +
                  f"[-] -> {name}.db <- File Not Exist !!! " + RESET + Back.RESET)
            conn = sqlite3.connect(f"{BASE_DB_PATH}{name}.db")
            if name == "yeswehack":
                query = """
                CREATE TABLE "yeswehack" (
                        "ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "name"	TEXT NOT NULL,
                        "submit"	TEXT NOT NULL,
                        "logo"	TEXT NOT NULL,
                        "color"	TEXT NOT NULL,
                        "program_url"	TEXT NOT NULL,
                        "scope"	TEXT NOT NULL
                    );
                """
                conn.execute(query)
                conn.close()
            elif name == "hackerone":
                query = """
                CREATE TABLE "hackerone" (
                        "ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "name"	TEXT NOT NULL,
                        "submit"	TEXT NOT NULL,
                        "logo"	TEXT NOT NULL,
                        "color"	TEXT NOT NULL,
                        "program_url"	TEXT NOT NULL,
                        "in-scope"	TEXT NOT NULL,
                        "out-of-scope"	TEXT,
                        "allows_bounty_splitting"	TEXT NOT NULL
                    );
                """
                conn.execute(query)
                conn.close()
            elif name == "bugcrowd":
                query = """
                CREATE TABLE "bugcrowd" (
                        "ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "name"	TEXT NOT NULL,
                        "submit"	TEXT NOT NULL,
                        "color"	TEXT NOT NULL,
                        "logo"	TEXT NOT NULL,
                        "program_url"	TEXT NOT NULL,
                        "scope"	TEXT NOT NULL
                    );
                """
                conn.execute(query)
                conn.close()

            elif name == "intigriti":
                query = """
                CREATE TABLE "intigriti" (
                        "ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "name"	TEXT NOT NULL,
                        "submit"	TEXT NOT NULL,
                        "color"	TEXT NOT NULL,
                        "logo"	TEXT NOT NULL,
                        "program_url"	TEXT NOT NULL,
                        "scope"	TEXT NOT NULL
                    );
                    
                """
                conn.execute(query)
                conn.close()
        else:
            print(Back.BLACK + GREEN +
                  f"[+] -> {name}.db <- File Is Exist  !!! " + RESET + Back.RESET)


def exist(name: str, platform: str) -> bool:
    if platform == "HACKERONE":
        conn = sqlite3.connect(f"{BASE_DB_PATH}hackerone.db")
        check = conn.execute(
            f"SELECT ID FROM hackerone WHERE name = ? ", (name,)).fetchone()
        if check:
            return True

    elif platform == "BUGCROWD":
        conn = sqlite3.connect(f"{BASE_DB_PATH}bugcrowd.db")
        check = conn.execute(
            f"SELECT ID FROM bugcrowd WHERE name = ? ", (name,)).fetchone()
        if check:
            return True

    elif platform == "INTIGRITI":
        conn = sqlite3.connect(f"{BASE_DB_PATH}intigriti.db")
        check = conn.execute(
            f"SELECT ID FROM intigriti WHERE name = ? ", (name,)).fetchone()
        if check:
            return True
    elif platform == "YESWEHACK":
        conn = sqlite3.connect(f"{BASE_DB_PATH}yeswehack.db")
        check = conn.execute(
            f"SELECT ID FROM yeswehack WHERE name = ? ", (name,)).fetchone()
        if check:
            return True

    conn.close()


def insert_db(json_data: dict, platform: str) -> bool:
    if platform == "HACKERONE":
        conn = sqlite3.connect(f"{BASE_DB_PATH}hackerone.db")
        name = json_data["name"]
        submit = json_data["submit"]
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        inscope = json_data["in-scope"]
        outofscope = json_data["out-of-scope"]
        allows_bounty_splitting = json_data["allows_bounty_splitting"]
        cur = conn.cursor()
        query = f'INSERT INTO hackerone (name, submit, logo, color, program_url, "in-scope", "out-of-scope" , allows_bounty_splitting) VALUES (?,?,?,?,?,?,?,?);'
        check = cur.execute(query, (str(name), str(submit), str(
            logo), str(color), str(program_url), str(inscope), str(outofscope), str(allows_bounty_splitting)))
        conn.commit()
        if check:
            send_new_target_notification(json_data)
            return True
    elif platform == "BUGCROWD":
        conn = sqlite3.connect(f"{BASE_DB_PATH}bugcrowd.db")
        name = json_data["name"]
        submit = json_data["submit"]
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        scope = json_data["scopes"]
        cur = conn.cursor()
        query = f"INSERT INTO bugcrowd (name, submit, logo, color, program_url, scope) VALUES (?,?,?,?,?,?);"
        check = cur.execute(query, (str(name), str(submit), str(
            logo), str(color), str(program_url), str(scope)))
        conn.commit()
        if check:
            send_new_target_notification(json_data)
            return True

    elif platform == "INTIGRITI":
        conn = sqlite3.connect(f"{BASE_DB_PATH}intigriti.db")
        name = json_data["name"]
        submit = json_data["submit"]
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        scope = json_data["scope"]
        cur = conn.cursor()
        query = f"INSERT INTO intigriti (name, submit, logo, color , program_url, scope) VALUES (?,?,?,?,?,?);"
        check = cur.execute(query, (str(name), str(submit), str(
            logo), str(color), str(program_url), str(scope)))
        conn.commit()
        if check:
            send_new_target_notification(json_data)
            return True
    elif platform == "YESWEHACK":
        conn = sqlite3.connect(f"{BASE_DB_PATH}yeswehack.db")
        name = json_data["name"]
        submit = json_data["submit"]
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        scope = json_data["scope"]
        cur = conn.cursor()
        query = f"INSERT INTO yeswehack (name, submit, logo, color, program_url, scope) VALUES (?,?,?,?,?,?);"
        check = cur.execute(query, (str(name), str(submit), str(
            logo), str(color), str(program_url), str(scope)))
        conn.commit()
        if check:
            send_new_target_notification(json_data)
            return True

    conn.close()
    return False


def get_db_data_by_name(platform: str, name: str):
    conn = sqlite3.connect(f"{BASE_DB_PATH}{platform.lower()}.db")
    data = conn.execute(
        f"SELECT * FROM {platform.lower()} WHERE name = ?", (name,)).fetchone()
    if platform == "HACKERONE":
        name = data[1]
        submit = data[2]
        logo = data[3]
        colour = data[4]
        program_url = data[5]
        in_scope = data[6]
        out_of_scope = data[7]
        allows_bounty_splitting = data[8]
        target_information = {"platform": "HACKERONE", "name": name,
                              "submit": submit, "logo": logo, "color": colour, "program_url": program_url, "in-scope": in_scope, "out-of-scope": out_of_scope, "allows_bounty_splitting": allows_bounty_splitting}
    elif platform == "BUGCROWD":
        name = data[1]
        submit = data[2]
        logo = data[3]
        colour = data[4]
        program_url = data[5]
        scope = data[6]
        target_information = {"platform": "BUGCROWD", "name": name, "submit": submit,
                              "logo": logo, "color": colour, "program_url": program_url, "scopes": scope}
    elif platform == "INTIGRITI":
        name = data[1]
        submit = data[2]
        logo = data[3]
        colour = data[4]
        program_url = data[5]
        scope = data[6]
        target_information = {"platform": "INTIGRITI", "name": name, "submit": submit, "logo": logo,
                              "color": colour, "program_url": program_url, "scope": scope}

    elif platform == "YESWEHACK":
        name = data[1]
        submit = data[2]
        logo = data[3]
        colour = data[4]
        program_url = data[5]
        scope = data[6]
        target_information = {"platform": "YESWEHACK", "name": name, "submit": submit,
                              "logo": logo, "color": colour, "program_url": program_url, "scope": scope}

    conn.close()
    return target_information


def get_db_data_by_id(platform: str, id):
    conn = sqlite3.connect(f"{BASE_DB_PATH}{platform.lower()}.db")
    data = conn.execute(
        f"SELECT * FROM {platform.lower()} WHERE ID = ?", (id,)).fetchone()
    if platform == "HACKERONE":
        name = data[1]
        submit = data[2]
        logo = data[3]
        color = data[4]
        program_url = data[5]
        in_scope = data[6]
        out_of_scope = data[7]
        allows_bounty_splitting = data[8]
        target_information = {"platform": "HACKERONE", "name": name,
                              "submit": submit, "logo": logo, "color": color, "program_url": program_url, "in-scope": in_scope, "out-of-scope": out_of_scope, "allows_bounty_splitting": allows_bounty_splitting}
    elif platform == "BUGCROWD":
        name = data[1]
        submit = data[2]
        logo = data[4]
        color = data[3]
        program_url = data[5]
        scope = data[6]
        target_information = {"platform": "BUGCROWD", "name": name, "submit": submit,
                              "logo": logo, "color": color, "program_url": program_url, "scopes": scope}
    elif platform == "INTIGRITI":
        name = data[1]
        submit = data[2]
        logo = data[4]
        color = data[3]
        program_url = data[5]
        scope = data[6]
        target_information = {"platform": "INTIGRITI", "name": name, "submit": submit, "logo": logo,
                              "color": color, "program_url": program_url, "scope": scope}

    elif platform == "YESWEHACK":
        name = data[1]
        submit = data[2]
        logo = data[3]
        color = data[4]
        program_url = data[5]
        scope = data[6]
        target_information = {"platform": "YESWEHACK", "name": name, "submit": submit,
                              "logo": logo, "color": color, "program_url": program_url, "scope": scope}

    conn.close()
    return target_information


def get_db_id(platform: str, name: str):
    conn = sqlite3.connect(f"{BASE_DB_PATH}{platform.lower()}.db")
    query = f"SELECT ID FROM {platform.lower()} WHERE name like ?"
    data = conn.execute(query, ('%' + name + '%',)).fetchone()
    conn.close()
    return data[0]


def update(json_data: dict, platform: str, info="", out_info=""):
    if platform == "HACKERONE":
        conn = sqlite3.connect(f"{BASE_DB_PATH}hackerone.db")
        ID = get_db_id(name=str(json_data["name"]), platform="HACKERONE")
        name = json_data['name']
        submit = json_data["submit"]
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        inscope = json_data["in-scope"]
        outofscope = json_data["out-of-scope"]
        allows_bounty_splitting = json_data["allows_bounty_splitting"]
        cur = conn.cursor()
        query = f'UPDATE hackerone SET submit = ?, color = ?, logo = ?, program_url = ?, "in-scope" = ?, "out-of-scope" = ? , allows_bounty_splitting = ? WHERE name = ?;'
        check = cur.execute(query, (str(submit), str(color), str(
            logo), str(program_url), str(inscope), str(outofscope), str(allows_bounty_splitting), str(name)))
        conn.commit()
        if check:
            for i in info:
                send_update_notification(
                    ID, platform=platform, info=i, msg=SCOPE_UPDATE_TITLE)

            for o in out_info:
                send_update_notification(
                    ID, platform=platform, info=o, msg=OUT_OF_SCOPE_UPDATE)
            return True

    elif platform == "BUGCROWD":
        conn = sqlite3.connect(f"{BASE_DB_PATH}bugcrowd.db")
        ID = get_db_id(name=str(json_data["name"]), platform="BUGCROWD")
        name = json_data['name']
        submit = json_data["submit"]
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        scope = json_data["scopes"]
        cur = conn.cursor()
        query = f"UPDATE bugcrowd SET submit = ?, logo = ?, color = ?, program_url = ?, scope = ? WHERE ID = ?;"
        check = cur.execute(query, (str(submit), str(
            logo), str(color), str(program_url), str(scope), ID))
        conn.commit()
        if check:
            for i in info:
                send_update_notification(
                    ID, platform=platform, info=i, msg=SCOPE_UPDATE_TITLE)
            return True

    elif platform == "INTIGRITI":
        conn = sqlite3.connect(f"{BASE_DB_PATH}intigriti.db")
        ID = get_db_id(name=str(json_data["name"]), platform="INTIGRITI")
        submit = json_data["submit"]
        name = json_data['name']
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        scope = json_data["scope"]
        cur = conn.cursor()
        query = f"UPDATE intigriti SET submit = ?, logo = ?, color = ?, program_url = ?, scope = ? WHERE ID = ?;"
        check = cur.execute(query, (str(submit), str(
            logo), str(color), str(program_url), str(scope), ID))
        conn.commit()
        if check:
            for i in info:
                send_update_notification(
                    ID, platform=platform, info=i, msg=SCOPE_UPDATE_TITLE)
            return True

    elif platform == "YESWEHACK":
        conn = sqlite3.connect(f"{BASE_DB_PATH}yeswehack.db")
        ID = get_db_id(name=str(json_data["name"]), platform="YESWEHACK")
        submit = json_data["submit"]
        name = json_data['name']
        logo = json_data["logo"]
        color = json_data["color"]
        program_url = json_data["program_url"]
        scope = json_data["scope"]
        cur = conn.cursor()
        query = f"UPDATE yeswehack SET submit = ?, logo = ?, color = ?, program_url = ?, scope = ? WHERE ID = ?;"
        check = cur.execute(query, (str(submit), str(
            logo), str(color), str(program_url), str(scope), ID))
        conn.commit()
        if check:
            for i in info:

                send_update_notification(
                    ID, platform=platform, info=i, msg=SCOPE_UPDATE_TITLE)
            return True

    conn.close()
    return False


def compare(json_data: dict, db_data, platform):
    if platform == "HACKERONE":
        info = []
        out_info = []
        in_olds = db_data["in-scope"]
        out_olds = db_data["out-of-scope"]
        if str(json_data["in-scope"]) != str(db_data["in-scope"]) or str(json_data["out-of-scope"]) != str(db_data["out-of-scope"]):
            for ins in json_data["in-scope"]:
                if str(ins).strip() not in in_olds:
                    info.append(str(ins).strip())
                else:
                    continue
            for oos in json_data["out-of-scope"]:
                if str(oos) not in out_olds:
                    out_info.append(str(oos).strip())
            update(json_data=json_data, platform="HACKERONE",
                   info=info, out_info=out_info)

    elif platform == "BUGCROWD":
        info = []
        in_olds = db_data["scopes"]
        if str(json_data["scopes"]) != str(db_data["scopes"]):
            for ins in json_data["scopes"]:
                if str(ins).strip() not in in_olds:
                    info.append(str(ins).strip())
            update(json_data=json_data, platform="BUGCROWD", info=info)

    elif platform == "INTIGRITI":
        info = []
        in_olds = db_data["scope"]
        if str(json_data["scope"]) != str(db_data["scope"]):
            for ins in json_data["scope"]:
                if str(ins).strip() not in in_olds:
                    info.append(str(ins).strip())
            update(json_data=json_data, platform="INTIGRITI", info=info)
    elif platform == "YESWEHACK":
        info = []
        in_olds = db_data["scope"]

        if str(json_data["scope"]) != str(db_data["scope"]):
            for ins in json_data["scope"]:
                if str(ins).strip() not in in_olds:
                    info.append(str(ins).strip())
            update(json_data=json_data, platform="YESWEHACK", info=info)


def send_update_notification(ID, platform, info="", msg=" SCOPE UPDATED "):
    if SEND_NOTIFICATION != "True":
        return ""
    data = get_db_data_by_id(id=ID, platform=platform)
    if platform == "HACKERONE":
        name = data["name"]
        logo_url = data["logo"]
        program_url = data["program_url"]
        color = data["color"].replace("#", "")
        allows_bounty_splitting = data["allows_bounty_splitting"]
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        embed = DiscordEmbed(title=msg,
                             color=color)
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="Hackerone", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        embed.add_embed_field(
            name="INFO:", value=f"```{info}```", inline=False)
        embed.add_embed_field(
            name="BBP:", value=allows_bounty_splitting, inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()

    elif platform == "BUGCROWD":
        name = data["name"]
        logo_url = data["logo"]
        program_url = data["program_url"]
        color = data["color"].replace("#", "")
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        embed = DiscordEmbed(title=msg,
                             color=color)
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="BugCrowd", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        embed.add_embed_field(
            name="INFO:", value=f"```{info}```", inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()
    elif platform == "INTIGRITI":
        name = data["name"]
        logo_url = data["logo"]
        program_url = data["program_url"]
        color = data["color"].replace("#", "")
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        embed = DiscordEmbed(title=msg,
                             color=color)
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="Intigriti", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        embed.add_embed_field(
            name="INFO:", value=f"```{info}```", inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()
    elif platform == "YESWEHACK":
        name = data["name"]
        logo_url = data["logo"]
        program_url = data["program_url"]
        color = data["color"].replace("#", "")
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        embed = DiscordEmbed(title=msg, color=color)
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="Yeswehack", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        embed.add_embed_field(
            name="INFO:", value=f"```{info}```", inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()


def telegram(URL):
    pass


def send_new_target_notification(json_data):
    if SEND_NOTIFICATION != "True":
        return ""
    platform = json_data["platform"]
    if platform == "HACKERONE":
        name = json_data["name"]
        logo_url = json_data["logo"]
        program_url = json_data["program_url"]
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        inscope = json_data["in-scope"]
        allows_bounty_splitting = json_data["allows_bounty_splitting"]
        scope = ""
        for t in inscope:
            scope += f"\n [+] {t} \n"

        embed = DiscordEmbed(title=NEW_TARGET_TITLE,
                             color=json_data["color"].replace("#", ""))
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="Hackerone", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        embed.add_embed_field(
            name="BBP:", value=allows_bounty_splitting, inline=False)

        webhook.add_embed(embed)
        response = webhook.execute()

    elif platform == "BUGCROWD":
        name = json_data["name"]
        logo_url = json_data["logo"]
        program_url = json_data["program_url"]
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        inscope = json_data["scopes"]
        scope = ""
        for t in inscope:
            scope += f"\n [+] {t} \n"

        embed = DiscordEmbed(title=NEW_TARGET_TITLE,
                             color=json_data["color"].replace("#", ""))
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="BugCrowd", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()
    elif platform == "INTIGRITI":
        name = json_data["name"]
        logo_url = json_data["logo"]
        program_url = json_data["program_url"]
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        inscope = json_data["scope"]
        scope = ""
        for t in inscope:
            scope += f"\n [+] {t} \n"

        embed = DiscordEmbed(title=NEW_TARGET_TITLE,
                             color=json_data["color"].replace("#", ""))
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="Intigriti", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()
    elif platform == "YESWEHACK":
        name = json_data["name"]
        logo_url = json_data["logo"]
        program_url = json_data["program_url"]
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        inscope = json_data["scope"]
        embed = DiscordEmbed(title=NEW_TARGET_TITLE,
                             color=json_data["color"].replace("#", ""))
        embed.set_thumbnail(url=logo_url)
        embed.add_embed_field(
            name="Platform:", value="Yeswehack", inline=False)
        embed.add_embed_field(name="Program:", value=name, inline=False)
        embed.add_embed_field(name="URL:", value=program_url, inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()


def parser(json_list: list):
    for data in json_list:
        platform = data["platform"]
        name = data["name"]
        if not exist(name=name, platform=platform):
            insert_db(data, platform)
        else:
            db_data = get_db_data_by_name(platform=platform, name=name)
            compare(json_data=data, db_data=db_data, platform=platform)


# ------------------------------------ Run Watcher ----------------------------------------------#


def progress(msg):
    run_msg = f"[+] {msg} ."
    colors = [RED, GREEN, YELLOW, CYAN, MAGENTA, BLUE]
    backs = [Back.WHITE, Back.BLACK]
    for _ in range(15):
        run_msg = run_msg + "."
        print(random.choice(backs) + random.choice(colors) +
              f" {run_msg} " + Back.RESET + RESET)
        time.sleep(0.3)
        os.system("cls")


def main(checkdb):
    if PRINTING == "True":
        enablePrint()
        progress(msg="Running Watcher ")
    else:
        blockPrint()

    if checkdb:
        db_exist()
    if CHECK_HACKERONE == "True":
        parser(hackerone())
    if CHECK_BUGCROWD == "True":
        parser(bugcrowd())
    if CHECK_INTIGRITI == "True":
        parser(intigriti())
    if CHECK_YESWEHACK == "True":
        parser(yeswehack())


check_db = True
while True:
    main(checkdb=check_db)
    check_db = False
    print(" SLEEP START ")
    time.sleep(3600)
