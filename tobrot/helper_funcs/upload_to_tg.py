#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import asyncio
import os
import re
import time
import sys, subprocess, shlex
from subprocess import call
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram.types import (
    InputMediaDocument,
    InputMediaVideo,
    InputMediaAudio
)
from tobrot.helper_funcs.display_progress import (
    progress_for_pyrogram,
    humanbytes
)
from tobrot.helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from tobrot.helper_funcs.split_large_files import split_large_files
from tobrot.helper_funcs.copy_similar_file import copy_file

from tobrot import (
    TG_MAX_FILE_SIZE,
    EDIT_SLEEP_TIME_OUT,
    DOWNLOAD_LOCATION,
    DO_CAPTION_1,
    DO_CAPTION_2,
    DO_CAPTION_3,
    chan_ids,
    name_ids
)


async def upload_to_tg(
    message,
    local_file_name,
    from_user,
    dict_contatining_uploaded_files,
    edit_media=False,
    custom_caption=None
):
   
    LOGGER.info(local_file_name)
    m2=''
    if local_file_name.upper().endswith(("MKV","MP4")):
     input_file=local_file_name
     cmnd = f"ffprobe -loglevel error -select_streams s -show_entries stream_tags=title -of csv=p=0 {input_file}".split(" ")
     p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

     out, err =  p.communicate()
     p=out.decode("utf-8")
     cmnd = f"ffprobe -loglevel error -select_streams s -show_entries stream_tags=language -of csv=p=0 {input_file}".split(" ")
     p1 = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

     out1, err1 =  p1.communicate()
     q=out1.decode("utf-8")
     p2=p.split('\n')
     q2=q.split('\n')
     p2=[x for x in p2 if x]
     q2=[x for x in q2 if x]
     n1=len(p2)
     n2=len(q2)
     if n1 == n2 and n1 > 0:
      i=" , ".join(j  for j in p2)
      mux=f"<b>{i}</b>"
      m2 = f"<b>Muxed Subtitles : </b><a href='https://telegra.ph/Muxed-English-Subtitles-12-29-9'>{mux}</a>\n\n"
     else:
        stop=["und"]
        i = [s.lower() for s in q.split() if s.lower() not in stop]
        n3=len(i)
        if n3 > 0:
         mux= f"<b>{i}</b>"
         m2 = f"<b>Muxed Subtitles : </b><a href='https://telegra.ph/Muxed-English-Subtitles-12-29-9'>{mux}</a>\n\n"
        else:
         mux= f"<b>???? Muxed English Subtitles ????</b>"
         m2 = f"<a href='https://telegra.ph/Muxed-English-Subtitles-12-29-9'>{mux}</a>\n\n"
    m3 = f"<a href='http://t.me/kdramaupdates'>Ongoing</a> | <a href='http://t.me/dramaindexchannel'>Index</a> | <a href='http://t.me/Korean_dramas_world'>Completed</a> | <a href='http://t.me/TeamDnO'>D&O</a>"

    base_file_name = os.path.basename(local_file_name)
    base_new_name = os.path.splitext(base_file_name)[0]
    extension_new_name = os.path.splitext(base_file_name)[1]
    b = base_new_name
    if b[:5] == "[D&O]":
      caption_str = f"<code>{base_new_name}{DO_CAPTION_1}</code>{DO_CAPTION_2}<code>{extension_new_name}</code>\n\n<b>{m2}{m3}</b>"
    elif b[:5].lower() == "[dno]":
      caption_str = f"<code>{base_new_name}{DO_CAPTION_1}</code>@DnOMovies TG Group<code>{extension_new_name}</code>\n\n<b>{m2}</b>"
    elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV", "RAR", "7Z", "ZIP")):
      caption_str = f"<code>{base_new_name}{extension_new_name}</code>\n\n<b>{m3}</b>"
    
    elif b[:3] == "KDG" and local_file_name.lower().endswith(".mp4"):
      caption_str = f"<b>{base_new_name}{extension_new_name}\n\n@kdg_166 @korea_drama\n@kdgfiles</b>"
    elif b[:3] == "KDG" and local_file_name.lower().endswith(".mkv"):
      caption_str = f"<b>{base_new_name}{extension_new_name}\n\n@kdg_166 @korea_drama\n@kdgfiles\n\nMuxed English Subtitles\nPlay it via external player</b>"
    else:
      caption_str = f"{base_new_name}{extension_new_name}\n\n<b>{m2}{m3}</b>"
    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        directory_contents.sort()
        # number_of_files = len(directory_contents)
        LOGGER.info(directory_contents)
        new_m_esg = message
        if not message.photo:
            new_m_esg = await message.reply_text(
                "Found {} files".format(len(directory_contents)),
                quote=True
                # reply_to_message_id=message.message_id
            )
        for single_file in directory_contents:
            # recursion: will this FAIL somewhere?
            await upload_to_tg(
                new_m_esg,
                os.path.join(local_file_name, single_file),
                from_user,
                dict_contatining_uploaded_files,
                edit_media,
                caption_str
            )
    else:
        if os.path.getsize(local_file_name) > TG_MAX_FILE_SIZE:
            LOGGER.info("TODO")
            d_f_s = humanbytes(os.path.getsize(local_file_name))
            i_m_s_g = await message.reply_text(
                "Telegram does not support uploading this file.\n"
                f"Detected File Size: {d_f_s} ????\n"
                "\n???? trying to split the files ????????????"
            )
            splitted_dir = await split_large_files(local_file_name)
            totlaa_sleif = os.listdir(splitted_dir)
            totlaa_sleif.sort()
            number_of_files = len(totlaa_sleif)
            LOGGER.info(totlaa_sleif)
            ba_se_file_name = os.path.basename(local_file_name)
            await i_m_s_g.edit_text(
                f"Detected File Size: {d_f_s} ????\n"
                f"<code>{ba_se_file_name}</code> splitted into {number_of_files} files.\n"
                "trying to upload to Telegram, now ..."
            )
            for le_file in totlaa_sleif:
                # recursion: will this FAIL somewhere?
                await upload_to_tg(
                    message,
                    os.path.join(splitted_dir, le_file),
                    from_user,
                    dict_contatining_uploaded_files
                )
        else:
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                edit_media
            )
            if sent_message is not None:
                dict_contatining_uploaded_files[os.path.basename(local_file_name)] = sent_message.message_id
    # await message.delete()
    return dict_contatining_uploaded_files


async def upload_single_file(message, local_file_name, caption_str, from_user, edit_media):
   
   base_file_name=os.path.basename(local_file_name)
   if len(base_file_name) > 64 and base_file_name.lower().startswith(("@dramaost","[d&o]")):
     status_message = await message.reply_text("Renaming start")
     h=base_file_name
     c_h=local_file_name
     out_dir = os.path.dirname(os.path.abspath(local_file_name))
     g=f"opus opus2.0 aac aac2.0 ddp5.1 ddp2.0 ddp2 h264 h.264 x264 10bit 2017 2018 2019 2020 2021 nf webdl web-dl webrip webhd web-hd web-rip".split(" ")
     c=0
     f=h.lower()
     f = re.sub("_", '.', f)
     f = re.sub("web.dl", 'webdl', f)
     if f[:3] == "d&o" :
       f = re.sub("d&o", '[d&o]', f)
     for i in g :
       if len(f) <= 64:
            break
       if re.search(i,f):
         f = re.sub("."+i, '', f)
     if len(f)>64:
       f = re.sub("@dramaost.", '', f)
     p=f.split('.')
     s= '.'.join(i.capitalize() for i in p)
     s = re.sub("Nf", 'NF', s)
     s = re.sub("Web-dl", 'WEB-DL', s)
     s = re.sub("Webdl", 'WEB-DL', s)
     s = re.sub("Webrip", 'WEBRip', s)
     s = re.sub("Sh3lby", 'SH3LBY', s)
     s = re.sub("sh3lby", 'SH3LBY', s)
     s = re.sub("ost", 'OST', s)
     s = re.sub("Mkv", 'mkv', s)
     s = re.sub("d&o", 'D&O', s)
     s = re.sub("D&o", 'D&O', s)
     s = re.sub("S01e", 'S01E', s)
     s = re.sub("S02e", 'S02E', s)
     s = re.sub("S03e", 'S03E', s)
     s = re.sub("S04e", 'S04E', s)
     s = re.sub("X265", 'x265', s)
     s = re.sub("X264", 'x264', s)
     out_file_name = os.path.join(out_dir, s)
     os.rename(local_file_name,out_file_name)
     local_file_name=out_file_name
     await status_message.edit(f"Old Name - <code>{c_h}</code>\n\nNew Name - <code>{local_file_name}</code>")
   elif not base_file_name.lower().startswith(("kdg")) and re.search('_',base_file_name.lower()):
    await message.reply_text(f"<code>{local_file_name}</code>\n\nfile name contain underscore please rename it")
   else:
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    sent_message = None
    start_time = time.time()
    #
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION,
        "thumbnails",
        str(from_user) + ".jpg"
    )
    LOGGER.info(thumbnail_location)
    #
    try:
        message_for_progress_display = message
        if not edit_media:
            message_for_progress_display = await message.reply_text(
                "starting upload of {}".format(os.path.basename(local_file_name))
            )
        if local_file_name.upper().endswith(("WEBM","MP4")) and not local_file_name.upper().startswith(("KDG")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            #
            width = 0
            height = 0
            thumb_image_path = None
            if os.path.exists(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            else:
                thumb_image_path = await take_screen_shot(
                    local_file_name,
                    os.path.dirname(os.path.abspath(local_file_name)),
                    (duration / 2)
                )
                # get the correct width, height, and duration for videos greater than 10MB
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    # resize image
                    # ref: https://t.me/PyrogramChat/44663
                    # https://stackoverflow.com/a/21669827/4723940
                    Image.open(thumb_image_path).convert(
                        "RGB"
                    ).save(thumb_image_path)
                    img = Image.open(thumb_image_path)
                    # https://stackoverflow.com/a/37631799/4723940
                    img.resize((320, height))
                    img.save(thumb_image_path, "JPEG")
                    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            #
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send video
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaVideo(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        width=width,
                        height=height,
                        duration=duration,
                        supports_streaming=True
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_video(
                    video=local_file_name,
                    # quote=True,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    width=width,
                    height=height,
                    thumb=thumb,
                    supports_streaming=True,
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)
        elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send audio
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaAudio(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        duration=duration,
                        performer=artist,
                        title=title
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_audio(
                    audio=local_file_name,
                    # quote=True,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    performer=artist,
                    title=title,
                    thumb=thumb,
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)
        else:
            base_file_name=os.path.basename(local_file_name)
            base_new_name = os.path.splitext(base_file_name)[0]
            extension_new_name = os.path.splitext(base_file_name)[1]
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            # if a file, don't upload "thumb"
            # this "diff" is a major derp -_- ????????????
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            #
            # send document
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaDocument(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html"
                    )
                    # quote=True,
                )
            elif base_file_name.lower().startswith(("@dramaost","[d&o]")):
                for l , s in zip(name_ids,chan_ids):
                 h=l.lower()
                 b=base_file_name.lower()
                 if re.search(h,b):
                  m4=f"<b>Join: {s}</b>"
                  caption_str = re.sub(".mkv",f".mkv</code>\n\n{m4}", caption_str)
                  break
                sent_message = await message.reply_document(
                    document=local_file_name,
                    # quote=True,
                    thumb=thumb,
                    caption=caption_str,
                    parse_mode="html",
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                    
                )
                  
            else:
                  sent_message = await message.reply_document(
                    document=local_file_name,
                    # quote=True,
                    thumb=thumb,
                    caption=caption_str,
                    parse_mode="html",
                    disable_notification=True,
                    # reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                    
                  )
                  
            if thumb is not None:
                os.remove(thumb)
    except Exception as e:
        await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
    else:
        if message.message_id != message_for_progress_display.message_id:
            await message_for_progress_display.delete()
    os.remove(local_file_name)
    return sent_message

