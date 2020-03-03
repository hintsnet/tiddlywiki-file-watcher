#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from datetime import *
import win32file
import win32con

wiki_dir = 'D:\\hintsnet-wudi\\products\\media-lib-tw'
path_to_watch = wiki_dir + '\\files'
path_of_tiddlers = wiki_dir + '\\tiddlers'
creator = 'pimgeek'
tags = '未分类'

def write_content_to_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as fh:
        return fh.write(content)

def generate_tiddler_content(media_file_name):
    new_tiddler_path = './files/' + media_file_name
    detected_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d%H%M%f")
    content =f"""_canonical_uri: {new_tiddler_path}
type: image/png
created: {detected_time}
creator: {creator}
modified: {detected_time}
modifier: {creator}
name: {media_file_name}
tags: {tags}
title: {media_file_name}
"""
    return content

def add_skinny_tiddler(media_file_name):
    ext = ('.gif','.ico','.jpeg','.jpg','.pdf','.png','.svg')
    if (media_file_name.lower().endswith(tuple(ext))):
        new_tiddler_path = os.path.join(path_of_tiddlers, media_file_name + ".tid")
        content = generate_tiddler_content(media_file_name)
        print(content)
        write_content_to_file(content, new_tiddler_path)
        return True

action_dic = {
 1: add_skinny_tiddler,
 5: add_skinny_tiddler
}

def update_tiddler(media_file_name, action_name):
    action = action_dic.get(action_name)
    if (action_name == 1 or action_name == 5):
        print("## ", media_file_name)
        action(media_file_name)

ACTIONS = {
  1: "被创建",
  2: "被删除",
  3: "内容被更新",
  4: "被重命名",
  5: "重命名为"
}

FILE_LIST_DIRECTORY = 0x0001

																  
print('监测文件夹：', path_to_watch)
hDir = win32file.CreateFile(
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)

while 1:
    results = win32file.ReadDirectoryChangesW(
        hDir,
        1024,
        True,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME,
        None,
        None)
    for action, filename in results:
        full_filename = os.path.join(path_to_watch, filename)
        print(full_filename, action, ACTIONS.get(action, "未知操作"))
        update_tiddler(filename, action)
