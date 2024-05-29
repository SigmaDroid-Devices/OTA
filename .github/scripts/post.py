#!/usr/bin/env python
#
# Python code which automatically posts Message in a Telegram Group if any new update is found.
# Intended to be run on every push
# USAGE : python3 post.py
# See README for more.
#
# Copyright (C) 2024 PrajjuS <theprajjus@gmail.com>
#
# Credits: Ashwin DS <astroashwin@outlook.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import telebot
import os
import json
import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep
from typing import List

# Get configs from workflow secrets
def getConfig(config_name: str):
    return os.getenv(config_name)
try:
    BOT_TOKEN = getConfig("BOT_TOKEN")
    CHAT_IDS = [x for x in getConfig("CHAT_IDS").split(" ")]
except KeyError:
    print("Fill all the configs plox..\nExiting...")
    exit(0)

REPOST_MD5 = getConfig("REPOST_MD5")

BANNER_PATH = "./assets/banner.png"

# Init bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# File directories
jsonDir = {
    "gapps": ".",
    "vanilla": "./vanila"
}
idDir = ".github/scripts"

# Store IDs in a file to compare
def update(IDs):
    with open(f"{idDir}/file_ids.txt", "w+") as log:
        for ids in IDs:
            log.write(f"{str(ids)}\n")

# Return IDs of all latest files from json files
def get_new_id():
    files = []
    file_id = []
    for type, dirName in jsonDir.items():
        for all in os.listdir(dirName):
            if all.endswith('.json'):
                files.append({"type": type, "dir": dirName, "file": all})
    for all_files in files:
        with open(f"{all_files['dir']}/{all_files['file']}", "r") as file:
            data = json.loads(file.read())['response'][0]
            file_id.append(data['md5'])
    return file_id

# Return previous IDs
def get_old_id():
    old_id = []
    with open(f"{idDir}/file_ids.txt", "r") as log:
        for ids in log.readlines():
            old_id.append(ids.replace("\n", ""))
    return old_id

# Remove elements in 2nd list from 1st, helps to find out which device got an update
def get_diff(new_id, old_id):
    first_set = set(new_id)
    sec_set = set(old_id)
    return list(first_set - sec_set)

# Grab needed info using ID of the file
def get_info(ID):
    FOUND = False
    files = []
    for type, dirName in jsonDir.items():
        for all in os.listdir(dirName):
            if all.endswith('.json'):
                files.append({"type": type, "dir": dirName, "file": all})
    for all_files in files:
        with open(f"{all_files['dir']}/{all_files['file']}", "r") as file:
            data = json.loads(file.read())['response'][0]
            if data['md5'] == ID:
                device = all_files['file']
                BUILD_TYPE = all_files['type']
                FOUND = True
                break
    if not FOUND:
        print(f"ID not found in repo: {ID}")
        exit(1)
    with open(f"{jsonDir[BUILD_TYPE]}/{device}") as device_file:
        info = json.loads(device_file.read())['response'][0]
        SIGMA_VERSION = info['version']
        DEVICE_NAME = info['device']
        DEVICE_CODENAME = device.split('.')[0]
        MAINTAINER = info['maintainer']
        SUPPORT_GROUP = info.get('support_group', None)
        PAYPAL = info['paypal']
        DOWNLOAD_URL = info['download']
        FILENAME = info['filename']
        DATE_TIME = datetime.datetime.fromtimestamp(int(info['timestamp']))
        MD5 = info['md5']
        SIZE = round(int(info['size'])/1000000000, 2)
        msg = ""
        msg += f"SigmaDroid Project {SIGMA_VERSION}\n"
        msg += f"Device Name: {DEVICE_NAME} ({DEVICE_CODENAME})\n"
        msg += f"Maintainer: {MAINTAINER}\n"
        msg += f"Support Group: {SUPPORT_GROUP}\n"
        msg += f"Date Time: {DATE_TIME}\n"
        msg += f"Build Type: {BUILD_TYPE}\n"
        # msg += f"Download URL: {DOWNLOAD_URL}\n"
        msg += f"Filename: {FILENAME}\n"
        msg += f"Size: {SIZE}G\n"
        msg += f"MD5: {MD5}\n\n"
        print(msg)
        return {
            "sigma_version": SIGMA_VERSION,
            "device": DEVICE_NAME,
            "codename": DEVICE_CODENAME,
            "maintainer": MAINTAINER,
            "support_group": SUPPORT_GROUP,
            "paypal": PAYPAL,
            "datetime": DATE_TIME,
            "build_type": BUILD_TYPE,
            "filename": FILENAME,
            "size": SIZE,
            "md5": MD5,
            "download": DOWNLOAD_URL
        }

# Prepare function for posting message in channel
def send_post(chat_id, image, caption, button):
    return bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=button)

# Prepare message format for channel
def message_content(information):
    msg = ""
    msg += f"<b>SigmaDroid</b> <code>v{information['sigma_version']}</code> | Android 14 - #OFFICIAL\n\n"
    msg += f"<b>Device:</b> <code>{information['device']} ({information['codename']})</code>\n"
    if isinstance(information['maintainer'], List):
        msg += f"<b>Maintainers:</b> "
        msg += " | ".join([f"<a href='https://t.me/{x}'>{x}</a>" for x in information['maintainer']])
        msg += "\n"
    else:
        msg += f"<b>Maintainer:</b> <a href='https://t.me/{information['maintainer']}'>{information['maintainer']}</a>\n"
    msg += f"<b>Build Date:</b> <code>{information['datetime']} UTC</code>\n"
    msg += f"<b>Build Type:</b> <code>{information['build_type']}</code>\n\n"
    filenameBase = information['filename'].replace(".zip", "")
    msg += f"<b>Release Notes:</b> <a href='https://raw.githubusercontent.com/SigmaDroid-devices/OTA/sigma-14.2/release_notes.txt'>Here</a>\n"
    msg += f"<b>Screenshots:</b> <a href='https://sigmadroid.xyz/Screenshots'>Here</a>\n"
    msg += f"<b>Official Website:</b> <a href='https://sigmadroid.xyz'>Here</a>\n"
    msg += f"\n#{information['codename']} #SigmaDroid #Android14"
    return msg

# Prepare buttons for message
def button(information):
    support = information['support_group'] if information['support_group'] is not None else 'https://t.me/SigmaDroidROMChat'
    buttons = InlineKeyboardMarkup()
    buttons.row_width = 2
    button1 = InlineKeyboardButton(text="📢 Channel", url=f"https://t.me/SigmaDroidAnnouncements")
    button2 = InlineKeyboardButton(text="🤝 Support", url=support)
    button3 = InlineKeyboardButton(text="📝 Changelog", url=f"https://sigmadroid.xyz/downloads/Home/{information['codename'].capitalize()}/Changelogs/{information['filename'].replace('.zip', '')}-Changelog.txt")
    button4 = InlineKeyboardButton(text="📥 Download", url=f"https://sigmadroid.xyz/downloads/Home/{information['codename'].capitalize()}/OTAs/{information['filename']}")
    button5 = InlineKeyboardButton(text="💰 Donate", url=information['paypal'])
    return buttons.add(button1, button2, button3, button4, button5)

# Send updates to channel and commit changes in repo
def tg_message():
    if REPOST_MD5:
        info = get_info(REPOST_MD5)
        for CHAT_ID in CHAT_IDS:
            with open(BANNER_PATH, "rb") as image:
                send_post(CHAT_ID, image, message_content(info), button(info))
        return
    commit_message = "Update new IDs and push OTA"
    commit_description = "Data for following device(s) were changed:\n"
    if len(get_diff(get_new_id(), get_old_id())) == 0:
        print("All are Updated\nNothing to do\nExiting...")
        sleep(2)
        exit(0)
    else:
        print(f"IDs Changed:\n{get_diff(get_new_id(), get_old_id())}\n\n")
        for devices in get_diff(get_new_id(), get_old_id()):
            info = get_info(devices)
            for CHAT_ID in CHAT_IDS:
                with open(BANNER_PATH, "rb") as image:
                    send_post(CHAT_ID, image, message_content(info), button(info))
            commit_description += f"- {info['device']} ({info['codename']})\n"
            sleep(5)
    update(get_new_id())
    open("commit_mesg.txt", "w+").write(f"SigmaDroid: {commit_message} [BOT]\n\n{commit_description}")


# Final stuffs
tg_message()
print("Successful")
sleep(2)