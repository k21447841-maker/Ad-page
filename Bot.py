import logging
import json
import time
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================
TOKEN = "8749571060:AAHdD9M_WihJS79OIX-WPLIQ5P9saEtnhNc"  # Apna token yahan dalo

# Adsterra Smartlink URL (aapki di hui URL)
ADSTERRA_URL = "https://www.effectivegatecpm.com/ebfsrhtwn3?key=641705b4c31d6dae463a86bf896e7792"

# Points System
POINTS_PER_AD = 10
LOGIN_BONUS = 10
WITHDRAW_RATIO = 1000  # 1000 points = 10 rupees

# ==================== DATABASE ====================
class Database:
    def __init__(self):
        self.users = {}  # In-memory database
        self.user_clicks = {}  # Track clicks per user
    
    def get_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                "points": 0,
                "total_earned": 0,
                "total_clicks": 0,
                "last_login": None,
                "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": None,
                "first_name": None
            }
        return self.users[user_id]
    
    def update_user(self, user_id, data):
        user_id = str(user_id)
        self.users[user_id] = data
    
    def add_points(self, user_id, points):
        user = self.get_user(user_id)
        user["points"] += points
        user["total_earned"] += points
        self.update_user(user_id, user)
        return user["points"]
    
    def record_click(self, user_id):
        user_id = str(user_id)
        if user_id not in self.user_clicks:
            self.user_clicks[user_id] = []
        self.user_clicks[user_id].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": "N/A",  # Can't get IP from Telegram
            "user_agent": "Telegram Bot"
        })
    
    def check_login_bonus(self, user_id):
        user = self.get_user(user_id)
        today = datetime.now().strftime("%Y-%m-%d")
        
        if user["last_login"] != today:
            user["last_login"] = today
            user["points"] += LOGIN_BONUS
            user["total_earned"] += LOGIN_BONUS
            self.update_user(user_id, user)
            return True, LOGIN_BONUS
        return False, 0

# Initialize database
db = Database()

# ==================== BOT CLASS ====================
class AdBot:
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username or "No username"
        first_name = update.effective_user.first_name or "User"
        
        # Save user info
        user = db.get_user(user_id)
        user["username"] = username
        user["first_name"] = first_name
        db.update_user(user_id, user)
        
        # Check login bonus
        bonus_given, bonus_points = db.check_login_bonus(user_id)
        
        # Get updated user data
        user = db.get_user(user_id)
        
        # Calculate rupees
        rupees = (user["points"] / 1000) * 10
        
        welcome_text = f"""🌟 **Welcome {first_name}!** 🌟

💰 **Your Balance:**
• Points: {user['points']}
• Rupees: ₹{rupees:.2f}
• Total Clicks: {user['total_clicks']}

"""
        if bonus_given:
            welcome_text += f"🎁 **Daily Login Bonus:** +{bonus_points} points!\n"
        
        welcome_text += f"""
📌 **How to Earn:**
1️⃣ Click "Watch Ad" button
2️⃣ Open the ad link
3️⃣ Get 10 points instantly!

💎 **Withdrawal:** Coming Soon!
   1000 Points = ₹10
   Minimum: 5000 Points

📊 **Your Stats:**
• Total Earned: {user['total_earned']} points
• Joined: {user['join_date']}
"""
        
        keyboard = [
            [InlineKeyboardButton("📺 Watch Ad & Earn 10 Points", callback_data='watch_ad')],
            [InlineKeyboardButton("📊 My Stats", callback_data='stats')],
            [InlineKeyboardButton("💸 Withdraw (Coming Soon)", callback_data='withdraw')],
            [InlineKeyboardButton("👥 Refer Friends", callback_data='refer')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def watch_ad(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        # Add points
        new_total = db.add_points(user_id, POINTS_PER_AD)
        
        # Record click
        db.record_click(user_id)
        
        # Update total clicks
        user = db.get_user(user_id)
        user["total_clicks"] += 1
        db.update_user(user_id, user)
        
        # Calculate rupees
        rupees = (new_total / 1000) * 10
        
        # Create ad button with Adsterra URL
        keyboard = [[
            InlineKeyboardButton(
                "🔗 Click Here to Watch Ad",
                url=ADSTERRA_URL
            )
        ]]
        
        # Add back button
        keyboard.append([
            InlineKeyboardButton("🔙 Back to Menu", callback_data='back')
        ])
        
        await query.edit_message_text(
            f"✅ **+{POINTS_PER_AD} Points Added!**\n\n"
            f"💰 **New Balance:**\n"
            f"• Points: {new_total}\n"
            f"• Rupees: ₹{rupees:.2f}\n\n"
            f"📊 **Today's Clicks:** {user['total_clicks']}\n\n"
            f"👇 **Click below to watch ad:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        # Get user's click history
        clicks = db.user_clicks.get(str(user_id), [])
        today_clicks = len([c for c in clicks if c['time'].startswith(datetime.now().strftime("%Y-%m-%d"))])
        
        rupees = (user["points"] / 1000) * 10
        total_rupees = (user["total_earned"] / 1000) * 10
        
        stats_text = f"""📊 **Your Detailed Stats**

**💰 Balance:**
• Points: {user['points']}
• Rupees: ₹{rupees:.2f}
• Total Earned: {user['total_earned']} points
• Total Value: ₹{total_rupees:.2f}

**🎯 Activity:**
• Total Clicks: {user['total_clicks']}
• Today's Clicks: {today_clicks}
• Last Login: {user.get('last_login', 'Never')}

**💎 Withdrawal Info:**
• Status: Coming Soon
• Rate: 1000 Points = ₹10
• Minimum: 5000 Points
• You need: {max(0, 5000 - user['points'])} more points

**📅 Account:**
• Joined: {user['join_date']}
• Username: @{user['username']}
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
        await query.edit_message_text(
            stats_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def withdraw(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if user["points"] >= 5000:
            text = """💸 **Withdrawal Request**

✅ **You are eligible for withdrawal!**

📝 **Coming Soon Feature**
Withdrawal system is under development.

You will be able to withdraw via:
• UPI (Google Pay, PhonePe, Paytm)
• Bank Transfer
• Cryptocurrency

**Stay tuned for updates!** 🚀
"""
        else:
            needed = 5000 - user["points"]
            text = f"""💸 **Withdrawal**

❌ **Not eligible yet!**

• Current Points: {user['points']}
• Points Needed: {needed}
• Minimum Required: 5000

💎 **Keep earning!**
Watch more ads to reach 5000 points.

**Coming Soon:** Withdrawal system
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def refer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        bot_username = (await context.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        
        text = f"""👥 **Referral Program**

🎁 **Earn 20% from referrals!**

**Your Referral Link:**
`{referral_link}`

**How it works:**
• Share this link with friends
• When they join, you earn 20% of their earnings
• Instant commission
• No limits!

**Coming Soon:** Full referral tracking
"""
        
        keyboard = [
            [InlineKeyboardButton("🔗 Share Link", url=f"https://t.me/share/url?url={referral_link}")],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        text = """❓ **Help & Guide**

**📌 How to Earn:**
1. Click "Watch Ad" button
2. Open the ad link
3. Get 10 points instantly
4. Repeat daily!

**💰 Points System:**
• Watch Ad: +10 points
• Daily Login: +10 points
• Referral: 20% commission

**💎 Withdrawal:**
• Coming Soon!
• Rate: 1000 Points = ₹10
• Minimum: 5000 Points

**📊 Daily Limit:**
• No limit! Watch as many ads as you want

**⚠️ Note:**
• Points are saved automatically
• Daily bonus resets at midnight
• One click = one point

Need help? Contact @admin
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        # Check login bonus
        db.check_login_bonus(user_id)
        user = db.get_user(user_id)
        
        rupees = (user["points"] / 1000) * 10
        
        text = f"""🌟 **Welcome Back!** 🌟

💰 **Balance:**
• Points: {user['points']}
• Rupees: ₹{rupees:.2f}
• Clicks: {user['total_clicks']}
"""
        
        keyboard = [
            [InlineKeyboardButton("📺 Watch Ad & Earn 10 Points", callback_data='watch_ad')],
            [InlineKeyboardButton("📊 My Stats", callback_data='stats')],
            [InlineKeyboardButton("💸 Withdraw (Coming Soon)", callback_data='withdraw')],
            [InlineKeyboardButton("👥 Refer Friends", callback_data='refer')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == 'watch_ad':
            await self.watch_ad(update, context)
        elif query.data == 'stats':
            await self.stats(update, context)
        elif query.data == 'withdraw':
            await self.withdraw(update, context)
        elif query.data == 'refer':
            await self.refer(update, context)
        elif query.data == 'help':
            await self.help(update, context)
        elif query.data == 'back':
            await self.back(update, context)
    
    async def track_clicks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Track when users click on ad links"""
        # This is called when user clicks any button with URL
        # We can track it here
        pass
    
    def run(self):
        app = Application.builder().token(TOKEN).build()
        
        # Command handlers
        app.add_handler(CommandHandler("start", self.start))
        
        # Callback handlers
        app.add_handler(CallbackQueryHandler(self.button_handler))
        
        print("="*60)
        print("🤖 ADSTERRA SMARTLINK BOT")
        print("="*60)
        print(f"Adsterra URL: {ADSTERRA_URL}")
        print(f"Points per ad: {POINTS_PER_AD}")
        print(f"Login Bonus: {LOGIN_BONUS}")
        print(f"Withdrawal: 1000 points = ₹10")
        print("="*60)
        print("Bot is running... Press Ctrl+C to stop")
        print("="*60)
        
        app.run_polling()

# ==================== RUN ====================
if __name__ == "__main__":
    if TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        TOKEN = input("Enter your Telegram Bot Token: ").strip()
    
    bot = AdBot()
    bot.run()
