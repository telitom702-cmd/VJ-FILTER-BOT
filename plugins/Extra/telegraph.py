# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

def upload_image_requests(image_path):
    upload_url = "https://envs.sh/index.php" # এখানে এন্ডপয়েন্ট ঠিক করা হয়েছে

    try:
        with open(image_path, 'rb') as file:
            files = {'file': file} 
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                # সার্ভার কী রিটার্ন করছে তা চেক করা
                response_text = response.text.strip()
                
                # envs.sh সাধারণত লিংকটি টেক্সট হিসেবে দেয়, তাই এটি সরাসরি নেওয়া হলো
                if response_text.startswith("http"):
                    return response_text
                else:
                    print(f"Unexpected response: {response_text}")
                    return None
            else:
                print(f"Upload failed with status code {response.status_code}")
                return None  # print এর বদলে None রিটার্ন করা হয়েছে

    except Exception as e:
        print(f"Error during upload: {e}")
        return None

@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    t_msg = await bot.ask(chat_id = update.from_user.id, text = "Now Send Me Your Photo Or Video Under 5MB To Get Media Link.")
    if not t_msg.media:
        return await update.reply_text("**Only Media Supported.**")
    path = await t_msg.download()
    uploading_message = await update.reply_text("<b>ᴜᴘʟᴏᴀᴅɪɴɢ...</b>")
    try:
        image_url = upload_image_requests(path)
        if not image_url:
            return await uploading_message.edit_text("**Failed to upload file.**")
    except Exception as error:
        await uploading_message.edit_text(f"**Upload failed: {error}**")
        return
    await uploading_message.edit_text(
        text=f"<b>Link :-</b>\n\n<code>{image_url}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Open Link", url=image_url),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={image_url}")
            ],[
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]])
    )
