#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

# the secret configuration specific things
if bool(os.environ.get("ENV", False)):
    from tobrot.sample_config import Config
else:
    from tobrot.config import Config


# TODO: is there a better way?
TG_BOT_TOKEN = Config.TG_BOT_TOKEN
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
AUTH_CHANNEL = Config.AUTH_CHANNEL
DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION
EXEC_CMD_TRIGGER = Config.EXEC_CMD_TRIGGER
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
TG_MAX_FILE_SIZE = Config.TG_MAX_FILE_SIZE
FREE_USER_MAX_FILE_SIZE = Config.FREE_USER_MAX_FILE_SIZE
CHUNK_SIZE = Config.CHUNK_SIZE
DEF_THUMB_NAIL_VID_S = Config.DEF_THUMB_NAIL_VID_S
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
PROCESS_MAX_TIMEOUT = Config.PROCESS_MAX_TIMEOUT
ARIA_TWO_STARTED_PORT = Config.ARIA_TWO_STARTED_PORT
EDIT_SLEEP_TIME_OUT = Config.EDIT_SLEEP_TIME_OUT
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = Config.MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START
MAX_TG_SPLIT_FILE_SIZE = Config.MAX_TG_SPLIT_FILE_SIZE
PROCESS_RUNNING = "processing ..."
Leech_CMD_TRIGGER = Config.leech_CMD_TRIGGER
Ytdl_CMD_TRIGGER = Config.ytdl_CMD_TRIGGER
Status_CMD_TRIGGER = Config.status_CMD_TRIGGER
Cancel_CMD_TRIGGER = Config.cancel_CMD_TRIGGER
Eval_CMD_TRIGGER = Config.Eval_CMD_TRIGGER
Rename_CMD_TRIGGER = Config.rename_CMD_TRIGGER
Upload_CMD_TRIGGER = Config.upload_CMD_TRIGGER
Save_Thumb_CMD_TRIGGER = Config.save_Thumb_CMD_TRIGGER
Clear_thumb_CMD_TRIGGER =Config.clear_thumb_CMD_TRIGGER
