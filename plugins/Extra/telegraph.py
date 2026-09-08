# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

def upload_media_requests(file_path):
    # envs.sh এর পরিবর্তে 0x0.st ব্যবহার করা হলো, কারণ envs.sh অনেক সময় bot রিকোয়েস্ট ব্লক করে
    upload_url = "https://0x0.st"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        with open(file_path, 'rb') as file:
            files = {'file': file} 
            response = requests.post(upload_url, files=files, headers=headers, timeout=120)

            if response.status_code == 200:
                return response.text.strip() 
            else:
                print(f"Upload failed with status code {response.status_code}")
                return None

    except Exception as e:
        print(f"Error during upload: {e}")
        return None

@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    # bot.ask ব্যবহার করার সময় timeout দেওয়া ভালো, যাতে বট আটকে না থাকে
    try:
        t_msg = await bot.ask(
            chat_id=update.from_user.id, 
            text="**Now Send Me Your Photo Or Video Under 5MB To Get Media Link.**",
            timeout=300
        )
    except asyncio.TimeoutError:
        return await update.reply_text("**Time Out! You took too long to send the media.**")

    if not t_msg.media:
        return await update.reply_text("**Only Media Supported.**")
    
    # যদি মিডিয়া ভিডিও হয় এবং সেটি 5MB এর বেশি হয়
    if t_msg.video or t_msg.document:
        if t_msg.file_size > 5242880: # 5MB in bytes
            return await update.reply_text("**File size must be under 5MB.**")

    path = await t_msg.download()
    uploading_message = await update.reply_text("<b>ᴜᴘʟᴏᴀᴅɪɴɢ...</b>")
    
    try:
        # ফাংশন কল করা হচ্ছে
        media_url = upload_media_requests(path)
        
        if not media_url:
            return await uploading_message.edit_text("**Failed to upload file. Server rejected the request or timed out.**")
            
    except Exception as error:
        await uploading_message.edit_text(f"**Upload failed: {error}**")
        return
    finally:
        # লোকাল স্টোরেজ থেকে ফাইল ডিলিট করে স্পেস বাঁচানো হচ্ছে
        if os.path.exists(path):
            os.remove(path)

    await uploading_message.edit_text(
        text=f"<b>Link :-</b>\n\n<code>{media_url}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Open Link", url=media_url),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={media_url}")
            ],[
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]])
        )
