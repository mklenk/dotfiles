#! /usr/bin/env python3
"""
This program is designed to work in tandem with dunst and i3blocks to extend
the functionality of the existing i3blocks notification blocklet and allow
multiple notifications of different priority levels to stack and be displayed.

Copyright (C) 2014  Tomasz Kramkowski

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
 
import os
import sys
import json
 
path = os.environ["HOME"] + "/.cache/i3blocks-dunst/notifications"
strlimit = 114 # Maximum notification length (without message amount).
 
# Returns the full notification text.
def full_text(notification):
    if len(notification["summary"] + notification["body"]) + 1 > strlimit:
        return "[{}] {}".format(notification["summary"],
                                notification["body"])[:strlimit - 3] + "..."
    else:
        return "[{}] {}".format(notification["summary"], notification["body"])
 
# Returns the short notification text.
def short_text(notification):
    if len(notification["summary"]) > strlimit:
        return notification["summary"][:strlimit - 3] + "..."
    else:
        return notification["summary"]
 
# Get the colour a notification should have.
def color(notification):
    if notification["urgency"] == "CRITICAL":
        return "#FF0000"
    elif notification["urgency"] == "NORMAL":
        return "#00FF00"
    elif notification["urgency"] == "LOW":
        return "#FFFFFF"
    else:
        return "#0000FF"
 
# Load the notification buffer.
def load_notifications():
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    if not os.path.isfile(path):
        f = open(path, "w+")
    else:
        f = open(path, "r")
    global notifications
    try:
        notifications = json.load(f)
    except:
        notifications = list()
    f.close()
 
# Save the notification buffer.
def save_notifications():
    f = open(path, "w")
    json.dump(notifications, f)
    f.close()
 
# Check if called by i3blocks.
def calledby_i3blocks():
    for k in os.environ:
        if k.startswith("BLOCK_"):
            return True
    return False
 
# Get the top notification.
def gettop():
    if os.environ["BLOCK_INSTANCE"] == "OLDEST":
        return 0
    elif os.environ["BLOCK_INSTANCE"] == "URGENT_OLDEST":
        for k, v in enumerate(notifications):
            if v["urgency"] == "CRITICAL":
                return k
        for k, v in enumerate(notifications):
            if v["urgency"] == "NORMAL":
                return k
        for k, v in enumerate(notifications):
            if v["urgency"] == "LOW":
                return k
    elif os.environ["BLOCK_INSTANCE"] == "NEWEST":
        return len(notifications) - 1
    elif os.environ["BLOCK_INSTANCE"] == "URGENT_NEWEST":
        for k, v in reversed(list(enumerate(notifications))):
            if v["urgency"] == "CRITICAL":
                return k
        for k, v in reversed(list(enumerate(notifications))):
            if v["urgency"] == "NORMAL":
                return k
        for k, v in reversed(list(enumerate(notifications))):
            if v["urgency"] == "LOW":
                return k
    return 0
 
# Append notification from arguments.
def append_notification():
    notifications.append({
        "app"     : sys.argv[1],
        "summary" : sys.argv[2],
        "body"    : sys.argv[3],
        "icon"    : sys.argv[4],
        "urgency" : sys.argv[5]
    })
    save_notifications()
 
# Delete topmost notification.
def delete_top():
    notifications.pop(gettop())
    save_notifications()
 
# Delete all notifications.
def delete_all():
    notifications = list()
    save_notifications()
 
# Print topmost notification details.
def print_notification():
    top = gettop()
    amount = ""
 
    if len(notifications) > 1:
        amount = "({})".format(len(notifications))
    print(full_text(notifications[top]) + amount)
    print(short_text(notifications[top]) + amount)
    print(color(notifications[top]))
 
if __name__ == "__main__":
    load_notifications()
    if calledby_i3blocks():
        if len(notifications) > 0:
            if os.environ["BLOCK_BUTTON"] == "1": # Left click
                delete_top()
            elif os.environ["BLOCK_BUTTON"] == "3": # Right click
                delete_all()
 
        if len(notifications) > 0:
            print_notification()
    else:
        append_notification()
        os.system("pkill -RTMIN+12 i3blocks")
    sys.exit(0)
