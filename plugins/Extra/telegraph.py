# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# টেলিগ্রাফ সার্ভারে আপলোড করার ফাংশন
def upload_to_telegraph(file_path):
    url = "https://telegra.ph/upload"
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, files={'file': f}, timeout=120)
            
            if response.status_code == 200:
                res_json = response.json()
                if isinstance(res_json, list) and len(res_json) > 0:
                    # সফল হলে লিংক রিটার্ন করবে
                    return "https://telegra.ph" + res_json[0].get('src')
                else:
                    # সার্ভার এরর দিলে সেটা রিটার্ন করবে যাতে বুঝা যায়
                    return f"Error: {res_json}"
            else:
                return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    # ১. ইউজারকে মিডিয়া পাঠাতে বলা হচ্ছে
    try:
        t_msg = await bot.ask(
            chat_id=update.from_user.id, 
            text="**Now Send Me Your Photo Or Video Under 5MB To Get Media Link.**",
            timeout=300
        )
    except asyncio.TimeoutError:
        return await update.reply_text("**Time Out! You took too long to send the media.**")

    # ২. মিডিয়া চেক করা হচ্ছে
    if not t_msg.media:
        return await update.reply_text("**Only Media Supported.**")
    
    # ৩. ৫ মেগাবাইটের নিচে কিনা চেক করা হচ্ছে
    if t_msg.video or t_msg.document:
        if t_msg.file_size > 5242880: # 5MB in bytes
            return await update.reply_text("**File size must be under 5MB.**")

    uploading_message = await update.reply_text("<b>ᴜᴘʟᴏᴀᴅɪɴɢ...</b>")
    file_path = None
    
    try:
        # ৪. টেলিগ্রাম থেকে লোকাল সার্ভারে ফাইল ডাউনলোড করা হচ্ছে
        file_path = await t_msg.download()

        # ৫. ফাংশন কল করে টেলিগ্রাফে আপলোড করা হচ্ছে
        media_url = upload_to_telegraph(file_path)
        
        # ৬. চেক করা হচ্ছে লিংক আসছে নাকি এরর আসছে
        if not media_url or media_url.startswith("Error"):
            return await uploading_message.edit_text(f"**Failed to upload file.**\n`{media_url}`")
            
        # ৭. সফল হলে লিংক ও বাটন দেখানো হচ্ছে
        await uploading_message.edit_text(
            text=f"<b>Link :-</b>\n\n<code>{media_url}</code>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="Open Link", url=media_url),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={media_url}")
            ],[
                InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]])
        )
        
    except Exception as error:
        await uploading_message.edit_text(f"**Upload failed: {error}**")
        
    finally:
        # ৮. স্টোরেজ বাঁচানোর জন্য ফাইল ডিলিট করা হচ্ছে
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
