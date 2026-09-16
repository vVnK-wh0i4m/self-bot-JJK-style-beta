import discord
from discord.ext import commands
import asyncio
import random
import json
import os
import time
from datetime import datetime, timedelta

ECONOMY_FILE = "economy_data.json"
_economy_lock = asyncio.Lock()

def load_economy():
    if os.path.exists(ECONOMY_FILE):
        with open(ECONOMY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_economy(data):
    with open(ECONOMY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def get_user_data(user_id):
    async with _economy_lock:
        data = load_economy()
        uid = str(user_id)
        if uid not in data:
            data[uid] = {"balance": 0, "daily": 0, "inventory": []}
            save_economy(data)
        return data[uid]

async def update_user_data(user_id, new_data):
    async with _economy_lock:
        data = load_economy()
        data[str(user_id)] = new_data
        save_economy(data)

TRIVIA_QUESTIONS = [
    {"q": "Jujutsu Kaisen - Ai là Vua Nguyền hồn vĩ đại nhất?", "a": ["Sukuna", "sukuna"]},
    {"q": "Jujutsu Kaisen - Thuật thức mạnh nhất của Gojo là gì?", "a": ["Hollow Purple", "hollow purple", "Void", "Infinite Void"]},
    {"q": "One Piece - Trái ác quỷ của Luffy là gì?", "a": ["Gomu Gomu no Mi", "gomu gomu"]},
    {"q": "Naruto - Võ thuật mạnh nhất của Naruto?", "a": ["Rasengan", "rasengan"]},
    {"q": "Dragon Ball - Cấp Super Saiyan đầu tiên là?", "a": ["Super Saiyan", "SSJ", "ssj"]},
    {"q": "Attack on Titan - Titan Founding là của ai?", "a": ["Eren", "eren"]},
    {"q": "Demon Slayer - Breath of Water là gì?", "a": ["Hơi thở nước", "Water Breathing", "water"]},
    {"q": "Tokyo Ghoul - Quỷ kaku RC cell là gì?", "a": ["RC cell", "rc cell"]},
    {"q": "Sword Art Online - Sword Art Online diễn ra ở game nào?", "a": ["SAO", "sao", "Sword Art Online"]},
    {"q": "My Hero Academia - Quirk của Deku là gì?", "a": ["One For All", "one for all"]},
    {"q": "1 + 1 = ?", "a": ["2", "hai"]},
    {"q": "Thủ đô của Việt Nam là gì?", "a": ["Hà Nội", "ha noi"]},
    {"q": "2 * 6 = ?", "a": ["12", "hai mười hai"]},
    {"q": "Màu của bầu trời là gì?", "a": ["xanh", "xanh dương", "xanh da trời", "blue"]},
    {"q": "Con vật nào kêu 'meo meo'?", "a": ["mèo", "meo", "cat"]},
]

FACTS = [
    "Một ngày trên Sao Hỏa dài hơn một ngày trên Trái Đất 37 phút.",
    "Mực có 3 trái tim và máu màu xanh.",
    "Oncilla là loài mèo nhỏ nhất thế giới, nặng chỉ 1.2kg.",
    "Đường ruột người dài gấp 3-4 lần chiều cao cơ thể.",
    "Tháp Eiffel cao hơn 300 mét và nặng khoảng 10,000 tấn.",
    "Con đường dài nhất thế giới là Pan-American Highway, dài 30,000 km.",
    "Nước chiếm khoảng 71% bề mặt Trái Đất.",
    "Một cơn bão có thể giải phóng năng lượng tương đương 10 quả bom nguyên tử.",
    "Trung bình mỗi người ngủ khoảng 25 năm trong đời.",
    "Mặt trời chiếm 99.86% khối lượng của Hệ Mặt Trời.",
    "Chuồn chuồn có thể bay với tốc độ 56 km/h.",
    "Oxy là nguyên tố phổ biến nhất trong vỏ Trái Đất.",
    "Chó có thể ngửi mùi ung thư ở người.",
    "Núi Everest mọc thêm khoảng 4mm mỗi năm.",
    "Sâu bướm có thể ăn hết lá cây trong vài ngày.",
]

QUOTES = [
    '"Ta chính là Sukuna, Vua Nguyền hồn." — Sukuna',
    '"Tự do thực sự chỉ dành cho người mạnh." — Geto',
    '"Mọi thứ đều vô nghĩa nếu không có chú thuật." — Gojo',
    '"Ta sẽ tiêu diệt tất cả Nguyền hồn." — Yuji',
    '"Kết giới này là lãnh địa của ta!" — Gojo',
    '"Mạnh lên, hoặc bị nuốt chửng." — Todo',
    '"Đó là lý do ta ghét bọn weakling." — Sukuna',
    '"Hollow Purple!" — Gojo Satoru',
    '"Thế giới này không cần hai vị vua." — Sukuna',
    '"Tao sẽ phá hủy mọi thứ." — Mahito',
]

SHOP_ITEMS = {
    "bam_ngo": {"name": "Bành Ngô (Random Box)", "price": 500, "desc": "Mở ra item ngẫu nhiên"},
    "chuc_luc": {"name": "Chú Lực Túi (Balo +10)", "price": 1000, "desc": "+10 ô backpack"},
    "hoa_dieu": {"name": "Hóa Giải Đá (Reset Stats)", "price": 2000, "desc": "Reset chỉ số"},
    "nguyen_lieu": {"name": "Nguyên Liệu SSR", "price": 5000, "desc": "Vật phẩm hiếm"},
}

class EntertainmentSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="traloi")
    async def _traloi(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;32m🎮 PHÁP ĐÀN GIẢI TRÍ 🎮\033[0m
\033[1;37m**Chọn thuật thức:**\033[0m

\033[1;34m🎮 MINI GAMES\033[0m
\033[1;30m  {p}8ball / rps / trivia  \033[1;30m- Games\033[0m
\033[1;30m  {p}coinflip / number    \033[1;30m- Đoán số\033[0m

\033[1;32m💰 KINH TẾ\033[0m
\033[1;30m  {p}daily / bal / pay    \033[1;30m- Vàng\033[0m
\033[1;30m  {p}shop / inventory     \033[1;30m- Cửa hàng\033[0m

\033[1;33m🌟 VUI\033[0m
\033[1;30m  {p}fact / quote / meme  \033[1;30m- Vui\033[0m
\033[1;30m  {p}insult / compliment  \033[1;30m- Troll\033[0m
\033[1;30m  {p}avatar / banner      \033[1;30m- Ảnh\033[0m
```"""
        await ctx.send(menu)

    # ================= MINI GAMES =================

    @commands.command(name="8ball")
    async def _eight_ball(self, ctx, *, question: str):
        """Phép bói 8 bóng"""
        responses = [
            "🔮 Chắc chắn rồi!",
            "🔮 Không thể nào.",
            "🔮 Có vẻ đúng.",
            "🔮 Chưa chắc.",
            "🔮 Hỏi lại sau.",
            "🔮spirit nói không.",
            "🔮 Đồng ý!",
            "🔮 Tuyệt đối!",
            "🔮 Đừng có mơ.",
            "🔮spirit nói có!",
        ]
        await ctx.send(f"🎱 **Câu hỏi:** {question}\n**Trả lời:** {random.choice(responses)}")

    @commands.command(name="rps")
    async def _rps(self, ctx, choice: str = None):
        """Kéo búa bao"""
        if not choice:
            return await ctx.send("❌ Gõ `.rps rock`, `.rps paper` hoặc `.rps scissors`!", delete_after=5)
        choice = choice.lower()
        if choice not in ["rock", "paper", "scissors", "kéo", "búa", "bao"]:
            return await ctx.send("❌ Chọn: rock/paper/scissors (hoặc kéo/búa/bao)!", delete_after=5)
        mapping = {"kéo": "scissors", "búa": "rock", "bao": "paper"}
        choice = mapping.get(choice, choice)
        bot_choice = random.choice(["rock", "paper", "scissors"])
        emoji = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        if choice == bot_choice:
            result = "⚖️ **HÒA!**"
        elif wins[choice] == bot_choice:
            result = "🏆 **BẠN THẮNG!**"
        else:
            result = "💀 **BẠN THUA!**"
        await ctx.send(f"{emoji[choice]} **Bạn:** {choice} vs **Bot:** {bot_choice} {emoji[bot_choice]}\n{result}")

    @commands.command(name="trivia")
    async def _trivia(self, ctx):
        """Câu đố vui"""
        q = random.choice(TRIVIA_QUESTIONS)
        await ctx.send(f"❓ **{q['q']}\n(Trả lời bằng `.tra-loi-câu [câu trả lời]`) **")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.startswith(".tra-loi-câu ")
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            answer = msg.content[len(".tra-loi-câu "):].strip()
            if answer.lower() in [a.lower() for a in q["a"]]:
                await ctx.send("✅ **ĐÚNG RỒI!** Bạn thông minh lắm!")
            else:
                await ctx.send(f"❌ **SAI RỒI!** Đáp án: **{q['a'][0]}**")
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ **Hết giờ!** Đáp án: **{q['a'][0]}**")

    @commands.command(name="coinflip")
    async def _coinflip(self, ctx):
        """Toss đồng xu"""
        result = random.choice(["🪙 **Mặt正面 (Ngửa)!**", "🪙 **Mặt背面 (Sấp)!**"])
        await ctx.send(result)

    @commands.command(name="number")
    async def _guess_number(self, ctx, guess: int = None):
        """Đoán số 1-100"""
        if guess is None:
            return await ctx.send("❌ Gõ `.number [số]` để đoán!", delete_after=5)
        target = random.randint(1, 100)
        if guess == target:
            await ctx.send(f"🎉 **BINGO!** Số bí ẩn là **{target}**! Bạn thắng!")
        elif abs(guess - target) <= 5:
            await ctx.send(f"🔥 **GẦN RỒI!** Số bí ẩn là **{target}**. Bạn đoán {guess}.")
        else:
            await ctx.send(f"❌ **SAI!** Số bí ẩn là **{target}**. Bạn đoán {guess}.")

    # ================= KINH TẾ =================

    @commands.command(name="daily")
    async def _daily(self, ctx):
        """Nhận quà hàng ngày"""
        data = await get_user_data(ctx.author.id)
        now = time.time()
        last = data.get("daily", 0)
        if now - last < 86400:
            remaining = int(86400 - (now - last))
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            return await ctx.send(f"⏰ Bạn đã nhận rồi! Chờ **{hours}h {minutes}m** nữa.", delete_after=5)
        reward = random.randint(100, 500)
        data["balance"] = data.get("balance", 0) + reward
        data["daily"] = now
        await update_user_data(ctx.author.id, data)
        await ctx.send(f"💰 **Daily!** Bạn nhận **{reward}** vàng! Số dư: **{data['balance']}**")

    @commands.command(name="bal")
    async def _balance(self, ctx, target: discord.Member = None):
        """Xem số dư"""
        target = target or ctx.author
        data = await get_user_data(target.id)
        await ctx.send(f"💰 **{target.name}** có **{data.get('balance', 0)}** vàng.")

    @commands.command(name="pay")
    async def _pay(self, ctx, target: discord.Member = None, amount: int = None):
        """Chuyển tiền"""
        if not target or not amount:
            return await ctx.send("❌ Gõ `.pay [@user] [số tiền]`!", delete_after=5)
        if amount <= 0:
            return await ctx.send("❌ Số tiền phải lớn hơn 0!", delete_after=5)
        data = await get_user_data(ctx.author.id)
        if data.get("balance", 0) < amount:
            return await ctx.send("❌ Không đủ vàng!", delete_after=5)
        data["balance"] -= amount
        await update_user_data(ctx.author.id, data)
        target_data = await get_user_data(target.id)
        target_data["balance"] = target_data.get("balance", 0) + amount
        await update_user_data(target.id, target_data)
        await ctx.send(f"💸 **{ctx.author.name}** đã chuyển **{amount}** vàng cho **{target.name}**!")

    @commands.command(name="shop")
    async def _shop(self, ctx):
        """Cửa hàng"""
        lines = ["```ansi\n\033[1;33m🏪 CỬA HÀNG THUẬT THỨC\033[0m\n"]
        for key, item in SHOP_ITEMS.items():
            lines.append(f"\033[1;37m{item['name']}\033[0m | \033[1;32m{item['price']} vàng\033[0m | `{key}`")
            lines.append(f"  \033[1;30m{item['desc']}\033[0m")
        lines.append("\nGõ `.buy [tên key]` để mua!```")
        await ctx.send("\n".join(lines))

    @commands.command(name="buy")
    async def _buy(self, ctx, item_key: str = None):
        """Mua vật phẩm"""
        if not item_key:
            return await ctx.send("❌ Gõ `.buy [tên key]`!", delete_after=5)
        if item_key not in SHOP_ITEMS:
            return await ctx.send("❌ Không tồn tại vật phẩm!", delete_after=5)
        data = await get_user_data(ctx.author.id)
        item = SHOP_ITEMS[item_key]
        if data.get("balance", 0) < item["price"]:
            return await ctx.send(f"❌ Không đủ vàng! Cần **{item['price']}**, bạn có **{data.get('balance', 0)}**.", delete_after=5)
        data["balance"] -= item["price"]
        inv = data.get("inventory", [])
        inv.append(item_key)
        data["inventory"] = inv
        await update_user_data(ctx.author.id, data)
        await ctx.send(f"🛒 **Đã mua {item['name']}!** Số dư: **{data['balance']}**")

    @commands.command(name="inventory")
    async def _inventory(self, ctx, target: discord.Member = None):
        """Xem vật phẩm"""
        target = target or ctx.author
        data = await get_user_data(target.id)
        inv = data.get("inventory", [])
        if not inv:
            return await ctx.send(f"📦 **{target.name}** không có vật phẩm nào.")
        item_counts = {}
        for k in inv:
            item_counts[k] = item_counts.get(k, 0) + 1
        lines = [f"📦 **Vật phẩm của {target.name}:**\n"]
        for k, count in item_counts.items():
            name = SHOP_ITEMS.get(k, {}).get("name", k)
            lines.append(f"• {name} x{count}")
        await ctx.send("\n".join(lines))

    # ================= VUI & THÚ VỊ =================

    @commands.command(name="fact")
    async def _fact(self, ctx):
        """Fact thú vị"""
        await ctx.send(f"🧠 **Fact:** {random.choice(FACTS)}")

    @commands.command(name="quote")
    async def _quote(self, ctx):
        """Trích dẫn JJK"""
        await ctx.send(f"📜 {random.choice(QUOTES)}")

    @commands.command(name="meme")
    async def _meme(self, ctx):
        """Random meme"""
        memes = [
            "https://cdn.discordapp.com/attachments/1376174995230949446/1520297142709784626/From_Klickpin.com-_Printable_Wall_Art_Ideas_That_Make_Everyday_Better_29506-pin-id-730779477063900866.gif?ex=6a40ae8c&is=6a3f5d0c&hm=5f9ab89de47a1d586beda24cf5c18f73d6b83f850b416cc3b00afbd2059014f1&",
            "https://media.tenor.com/images/memes/sukuna-memes/sukuna-meme.gif",
        ]
        await ctx.send(random.choice(memes))

    @commands.command(name="insult")
    async def _insult(self, ctx, target: discord.Member = None):
        """Insult vui"""
        target = target or ctx.author
        insults = [
            f"{target.mention} IQ của bạn thấp hơn nhiệt độ phòng!",
            f"{target.mention} Bạn là lý do Darwin buồn!",
            f"{target.mention} Trí thông minh của bạn đang ngoại tuyến!",
            f"{target.mention} Bạn giống update Windows - chậm và phiền!",
            f"{target.mention} Não bạn đang trong chế độ tiết kiệm pin!",
        ]
        await ctx.send(random.choice(insults))

    @commands.command(name="compliment")
    async def _compliment(self, ctx, target: discord.Member = None):
        """Khen ngợi"""
        target = target or ctx.author
        compliments = [
            f"{target.mention} Bạn tuyệt vời như Sukuna!",
            f"{target.mention} Aura của bạn tỏa sáng!",
            f"{target.mention} Bạn là Special Grade sorcerer!",
            f"{target.mention} Cười lên, bạn đẹp trai/xinh gái lắm!",
            f"{target.mention} Bạn là reason server này vui!",
        ]
        await ctx.send(random.choice(compliments))

    @commands.command(name="avatar")
    async def _avatar(self, ctx, target: discord.Member = None):
        """Avatar đẹp"""
        target = target or ctx.author
        if target.avatar:
            await ctx.send(f"🖼️ **Avatar của {target.name}:**\n{target.avatar.url}")
        else:
            await ctx.send("❌ Đối tượng không có avatar!", delete_after=3)

    @commands.command(name="banner")
    async def _banner(self, ctx, target: discord.User = None):
        """Banner đẹp"""
        target = target or ctx.author
        try:
            user = await self.bot.fetch_user(target.id)
            if user.banner:
                await ctx.send(f"🖼️ **Banner của {target.name}:**\n{user.banner.url}")
            else:
                await ctx.send("❌ Đối tượng không có banner!", delete_after=3)
        except Exception:
            await ctx.send("❌ Không thể lấy banner!", delete_after=3)

async def setup(bot):
    await bot.add_cog(EntertainmentSystem(bot))
