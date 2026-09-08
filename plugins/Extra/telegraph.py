# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    # ১. ব্যবহারকারীকে মেসেজ পাঠানোর জন্য বলছি (timeout সহ যাতে বট হ্যাং না হয়)
    try:
        t_msg = await bot.ask(
            chat_id=update.from_user.id, 
            text="**Now Send Me Your Photo Or Video Under 5MB To Get Media Link.**",
            timeout=300
        )
    except asyncio.TimeoutError:
        return await update.reply_text("**Time Out! You took too long to send the media.**")

    # ২. মিডিয়া আছে কিনা চেক করা হচ্ছে
    if not t_msg.media:
        return await update.reply_text("**Only Media Supported.**")
    
    # ৩. ফাইল সাইজ ৫ মেগাবাইটের মধ্যে আছে কিনা চেক করা হচ্ছে
    if t_msg.video or t_msg.document:
        if t_msg.file_size > 5242880: # 5MB in bytes
            return await update.reply_text("**File size must be under 5MB.**")

    # ব্যবহারকারীকে আপলোড হওয়ার মেসেজ দেখানো হচ্ছে
    uploading_message = await update.reply_text("<b>ᴜᴘʟᴏᴀᴅɪɴɢ...</b>")
    file_path = None
    
    try:
        # ৪. টেলিগ্রামে ফাইল ডাউনলোড করা হচ্ছে
        file_path = await t_msg.download()

        # ৫. টেলিগ্রাফ সার্ভারে আপলোড করা হচ্ছে (Pyrogram এর বিল্ট-ইন ফিচার ব্যবহার করা হয়েছে)
        # এটি envs.sh বা 0x0.st এর চেয়ে অনেক বেশি ফাস্ট এবং সিকিউর
        media_url = await bot.upload_file(file=file_path)
        
        # আপলোড সফল হলে লিংক দেখানো হচ্ছে
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
        # যদি কোনো কারণে আপলোড ব্যর্থ হয়, তবে এরর মেসেজ দেখানো হচ্ছে
        await uploading_message.edit_text(f"**Upload failed: {error}**")
        
    finally:
        # ৬. লোকাল সার্ভার থেকে ফাইল ডিলিট করে স্টোরেজ বাঁচানো হচ্ছে
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
