<div align="center">

# ⚡ JJK-VVNK Bot ⚡

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py--self-2.0%2B-purple?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-6.4-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Discord Self Bot theo phong cách Jujutsu Kaisen với đầy đủ tính năng war, spam, nhạc, giải trí và quản lý.**

[📥 **Tải code (.zip)**](https://github.com/vVnK-wh0i4m/self-bot-JJK-style-beta/archive/refs/heads/main.zip) • [📦 **Clone repo**](https://github.com/vVnK-wh0i4m/self-bot-JJK-style-beta.git)

</div>

---

## ⚠️ Cảnh báo quan trọng

> **Self bot vi phạm Discord Terms of Service (ToS).** Sử dụng có thể dẫn đến tài khoản bị **khóa vĩnh viễn**. Hãy sử dụng **tài khoản phụ**, **KHÔNG** dùng tài khoản chính. Tác giả **không chịu trách nhiệm** về bất kỳ hậu quả nào.

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt và chạy](#-cài-đặt-và-chạy)
- [Cấu hình](#-cấu-hình)
- [Danh sách lệnh](#-danh-sách-lệnh)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Bản quyền và điều khoản](#-bản-quyền-và-điều-khoản)
- [FAQ](#-câu-hỏi-thường-gặp)

---

## 🌟 Giới thiệu

**JJK-VVNK Bot** (HostBot v6.4) là Discord Self Bot được xây dựng theo phong cách **Jujutsu Kaisen** với theme **"Domain Expansion: Infinite Void"**. Bot cung cấp bộ tính năng đa dạng:

- ⚔️ **War/Spam** - Tấn công, spam đa dạng
- 🎵 **Music** - Phát nhạc từ YouTube
- 🎮 **Fun/Games** - Giải trí, game mini
- 🛠️ **Utility** - Tiện ích quản lý
- 🛡️ **Admin** - Quản lý server
- 🃏 **Troll** - Các lệnh troll vui
- 🎯 **Nitro Sniper** - Tự động claim Nitro gift

**Điểm nổi bật:**
- 🚀 Cài đặt đơn giản chỉ với 1 click `Run.bat`
- 🔄 Tự động restart khi crash
- 🎨 Giao diện JJK aesthetic
- 📦 Tự động cài đặt thư viện

---

## 🚀 Tính năng

### ⚔️ War / Spam

| Tính năng | Mô tả |
|-----------|--------|
| `.vohahan [delay] [text]` | Spam tùy chỉnh 100 tin |
| `.thuong [delay]` | Spam từ ngon.txt |
| `.lienke [delay] [@user]` | Spam từ nhay.txt |
| `.hacmon [url] [delay] [text]` | Spam qua Webhook |
| `.khaitram` | Xóa toàn bộ kênh |
| `.huydiet` | Nuke server |

### 🎵 Music

| Tính năng | Mô tả |
|-----------|--------|
| `.play [link/ten]` | Phát nhạc từ YouTube |
| `.play-sa` | Phát "Stay Alive" |
| `.play-sh` | Phát "Styx Helix" |
| `.play-amk` | Phát "Akuma no Ko" |
| `.play-sp` | Phát "Specialz" |
| `.queue` | Xem hàng chờ |
| `.skip` | Bỏ qua bài hiện tại |
| `.stop` | Dừng nhạc + rời voice |
| `.loop` | Bật/tắt lặp bài |
| `.volume [1-100]` | Điều chỉnh âm lượng |

### 🎮 Giải trí

| Tính năng | Mô tả |
|-----------|--------|
| `.8ball [câu hỏi]` | Bói 8 bóng |
| `.rps [rock/paper/scissors]` | Kéo búa bao |
| `.trivia` | Câu đố vui |
| `.coinflip` | Đồng xu |
| `.number [1-100]` | Đoán số |
| `.daily` | Nhận vàng hàng ngày |
| `.bal` | Xem số dư |
| `.pay [@user] [so]` | Chuyển tiền |
| `.shop` / `.buy [item]` | Cửa hàng |
| `.avatar [@user]` | Xem avatar |
| `.banner [@user]` | Xem banner |

### 🛠️ Tiện ích

| Tính năng | Mô tả |
|-----------|--------|
| `.thauthi [token]` | Kiểm tra token |
| `.thanhduyet [so]` | Xóa tin nhắn |
| `.giapan` | Đóng DM |
| `.nguonluc` | Check ping |
| `.truytung [@user]` | Soi avatar |
| `.phian [@user]` | Soi banner |
| `.danhdinh [@user]` | Thông tin người dùng |
| `.ketgioi` | Thông tin server |
| `.dongan [emoji]` | Sao chép emoji |
| `.sao-an [server_id]` | Sao chép kênh |

### 🛡️ Quản lý

| Tính năng | Mô tả |
|-----------|--------|
| `.tram [user]` | Kick |
| `.phong [user]` | Ban |
| `.giai [user_id]` | Unban |
| `.diet` | Xóa kênh |
| `.tao [ten]` | Tạo kênh |
| `.danh [ten]` | Đổi tên server |

### 🃏 Troll

| Tính năng | Mô tả |
|-----------|--------|
| `.batdiet` | Game nhân phẩm |
| `.xucxac` | Xúc xắc |
| `.amhon [url]` | Phát nhạc vào Voice |
| `.truhon` | Rời Voice |
| `.fake [@user] [text]` | Giả mạo tin nhắn |
| `.donguyen` | Đo sức mạnh |
| `.vonghon` | Nhại lại tin nhắn |
| `.nguyenrua [@user]` | ÂmQue đối phương |
| `.batkhuat` | Tự phản hồi khi bị tag |

### 🎯 Auto Features

| Tính năng | Mô tả |
|-----------|--------|
| Nitro Sniper | Tự động claim Nitro gift |
| Cycle Status | Tự động chuyển status |
| Auto GIF | GIF tự động sau mỗi lệnh |
| Auto Delete | Xóa tin nhắn lệnh sau khi xử lý |

---

## 💻 Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|----------|
| Hệ điều hành | Windows 10+, macOS, Linux |
| Python | 3.8 trở lên |
| RAM | Tối thiểu 512MB |
| Ổ cứng | 500MB trống |
| Mạng | Kết nối internet ổn định |
| FFmpeg | Cần thiết cho tính năng phát nhạc |

---

## 📥 Cài đặt và chạy

### Cách 1: Dùng Run.bat (khuyến nghị - Windows)

1. **Tải code:**
   - [📥 Tải file ZIP](https://github.com/vVnK-wh0i4m/self-bot-JJK-style-beta/archive/refs/heads/main.zip)
   - Hoặc clone: `git clone https://github.com/vVnK-wh0i4m/self-bot-JJK-style-beta.git`

2. **Giải nén** thư mục `jjkvvnk-main`

3. **Double-click** file `Run.bat`

4. **Nhập Discord Token** khi được yêu cầu

5. Bot sẽ tự động:
   - Cài đặt thư viện
   - Tạo thư mục cần thiết
   - Khởi động bot
   - Tự restart khi crash

### Cách 2: Chạy thủ công

```bash
# Clone repo
git clone https://github.com/vVnK-wh0i4m/self-bot-JJK-style-beta.git
cd jjkvvnk-main

# Cài thư viện
pip install -r requirements.txt

# Chạy bot
python main.py
```

### Cách 3: Trên Hosting

> Xem hướng dẫn chi tiết tại [README của self-bot-cam](https://github.com/vVnK-wh0i4m/self-bot-cam/blob/main/README.md#cài-đặt-trên-hosting)

---

## ⚙️ Cấu hình

### File `config.json` (tự tạo bởi Run.bat)

```json
{
    "token": "DISCORD_TOKEN_CUA_BAN",
    "prefix": "."
}
```

### File `settings.json`

```json
{
    "bot_name": "HostBot",
    "author": "QU4N.TH3.D3V",
    "auto_gif": true,
    "status_cycle": [
        ".menu de mo Menu",
        "HostBot v6.2",
        "Dung .help de tro giup"
    ]
}
```

| Trường | Mô tả |
|--------|-------|
| `bot_name` | Tên hiển thị của bot |
| `author` | Tên tác giả |
| `auto_gif` | Bật/tắt GIF tự động |
| `status_cycle` | Danh sách status tự chuyển |
| `gif_responses` | URL GIF theo danh mục |

### Cách lấy Token Discord

> ⚠️ **CẢNH BÁO:** KHÔNG BAO GIỜ chia sẻ token.

1. Mở Discord trên trình duyệt
2. Nhấn `F12` → Tab **Network**
3. Tìm header `Authorization` → đó là token

---

## 💬 Danh sách lệnh

> Prefix mặc định: `.`

### 🔹 Lệnh chính

| Lệnh | Aliases | Mô tả |
|-------|---------|--------|
| `.menu` | - | Hiển thị menu chính |
| `.lanhdia` | - | Menu JJK style |
| `.info` | `.danhdinh` | Thông tin bot & server |
| `.ngung` | - | Dừng tất cả thuật thức |

### ⚔️ War / Spam

| Lệnh | Aliases | Mô tả | Ví dụ |
|-------|---------|-------|-------|
| `.raid` | - | Menu war | `.raid` |
| `.vohahan [delay] [text]` | `.spam` | Spam tùy chỉnh | `.vohahan 2 Hello` |
| `.thuong [delay]` | `.ngon` | Spam từ ngon.txt | `.thuong 1.5` |
| `.lienke [delay] [@user]` | `.nhay` | Spam từ nhay.txt | `.lienke 1 @user` |
| `.hacmon [url] [delay] [text]` | - | Spam Webhook | `.hacmon https://... 2 Hi` |
| `.ngucmon [voice_id]` | `.voice` | Treo Voice | `.ngucmon 123456` |
| `.loanvuc [voice_id] [delay]` | `.jl` | Spam join/leave | `.loanvuc 123456 1` |
| `.anpham [so] [emoji]` | `.react` | Reaction hàng loạt | `.anpham 10 👍` |
| `.khaitram` | `.xoa` | Xóa toàn bộ kênh | `.khaitram` |
| `.huydiet` | `.nuke` | Nuke server | `.huydiet` |

### 🎵 Nhạc

| Lệnh | Aliases | Mô tả | Ví dụ |
|-------|---------|-------|-------|
| `.nhac` | - | Menu nhạc | `.nhac` |
| `.play [link/ten]` | - | Phát nhạc từ YT | `.play Never Gonna Give You Up` |
| `.play-sa` | - | Phát "Stay Alive" | `.play-sa` |
| `.play-sh` | - | Phát "Styx Helix" | `.play-sh` |
| `.play-amk` | - | Phát "Akuma no Ko" | `.play-amk` |
| `.play-sp` | - | Phát "Specialz" | `.play-sp` |
| `.queue` | - | Xem hàng chờ | `.queue` |
| `.skip` | - | Bỏ qua bài | `.skip` |
| `.stop` | - | Dừng nhạc | `.stop` |
| `.now` | - | Bài đang phát | `.now` |
| `.loop` | - | Lặp bài | `.loop` |
| `.volume [1-100]` | - | Âm lượng | `.volume 50` |
| `.pause` | - | Tạm dừng | `.pause` |
| `.resume` | - | Tiếp tục | `.resume` |

### 🎮 Giải trí

| Lệnh | Aliases | Mô tả | Ví dụ |
|-------|---------|-------|-------|
| `.traloi` | - | Menu giải trí | `.traloi` |
| `.8ball [câu hỏi]` | `.boi` | Bói 8 bóng | `.8ball Toi co hanh phuc khong?` |
| `.rps [rock/paper/scissors]` | `.keobua` | Kéo búa bao | `.rps rock` |
| `.trivia` | `.doan` | Câu đố vui | `.trivia` |
| `.coinflip` | `.dongxu` | Đồng xu | `.coinflip` |
| `.number [1-100]` | `.sobian` | Đoán số | `.number 50` |
| `.daily` | `.qua` | Nhận vàng/ngày | `.daily` |
| `.bal` | `.vang` | Xem số dư | `.bal` |
| `.pay [@user] [so]` | - | Chuyển tiền | `.pay @user 100` |
| `.shop` | `.cuahang` | Cửa hàng | `.shop` |
| `.buy [item]` | - | Mua vật phẩm | `.buy sword` |
| `.inventory` | - | Vật phẩm | `.inventory` |
| `.fact` | - | Fact ngẫu nhiên | `.fact` |
| `.quote` | - | Quote ngẫu nhiên | `.quote` |
| `.meme` | - | Meme ngẫu nhiên | `.meme` |
| `.insult [@user]` | - | Chế giễu | `.insult @user` |
| `.compliment [@user]` | - | Khen ngợi | `.compliment @user` |
| `.avatar [@user]` | `.avt` | Xem avatar | `.avatar @user` |
| `.banner [@user]` | `.bv` | Xem banner | `.banner @user` |

### 🛠️ Tiện ích

| Lệnh | Aliases | Mô tả | Ví dụ |
|-------|---------|-------|-------|
| `.chucu` | - | Menu tiện ích | `.chucu` |
| `.thauthi [token]` | `.check` | Kiểm tra token | `.thauthi abc123` |
| `.thanhduyet [so]` | `.xoa` | Xóa tin nhắn | `.thanhduyet 100` |
| `.giapan` | `.dm` | Đóng DM | `.giapan` |
| `.nguonluc` | `.ping` | Check ping | `.nguonluc` |
| `.truytung [@user]` | `.soi` | Soi avatar | `.truytung @user` |
| `.phian [@user]` | `.soibv` | Soi banner | `.phian @user` |
| `.danhdinh [@user]` | `.info` | Info người dùng | `.danhdinh @user` |
| `.ketgioi` | `.sv` | Info server | `.ketgioi` |
| `.dongan [emoji]` | `.emoji` | Clone emoji | `.dongan :smile:` |
| `.sao-an [server_id]` | - | Clone kênh | `.sao-an 123456` |

### 🛡️ Quản lý

| Lệnh | Aliases | Mô tả | Ví dụ |
|-------|---------|-------|-------|
| `.quanly` | - | Menu quản lý | `.quanly` |
| `.tram [user]` | `.kick` | Kick | `.tram @user` |
| `.phong [user]` | `.ban` | Ban | `.phong @user` |
| `.giai [user_id]` | `.unban` | Unban | `.giai 123456` |
| `.diet` | `.clearch` | Xóa kênh | `.diet` |
| `.tao [ten]` | `.taokenh` | Tạo kênh | `.tao general` |
| `.danh [ten]` | `.rename` | Đổi tên server | `.danh NewServer` |

### 🃏 Troll

| Lệnh | Aliases | Mô tả | Ví dụ |
|-------|---------|-------|-------|
| `.troll` | - | Menu troll | `.troll` |
| `.batdiet` | `.ngauNhien` | Game nhân phẩm | `.batdiet` |
| `.xucxac` | - | Xúc xắc | `.xucxac` |
| `.amhon [url]` | `.nhacvao` | Phát nhạc vào VC | `.amhon https://...` |
| `.truhon` | `.roivoice` | Rời Voice | `.truhon` |
| `.fake [@user] [text]` | `.giamao` | Giả mạo tin nhắn | `.fake @user Hello` |
| `.donguyen` | `.chuluc` | Đo sức mạnh | `.donguyen` |
| `.vonghon` | `.nhai` | Nhại tin nhắn | `.vonghon` |
| `.nguyenrua [@user]` | `.amque` | ÂmQue | `.nguyenrua @user` |
| `.batkhuat` | `.phanhoi` | Auto reply khi tag | `.batkhuat` |

---

## 📁 Cấu trúc dự án

```
jjkvvnk/
├── main.py              # Entry point
├── Run.bat              # Launcher tự động (Windows)
├── config.json          # Token (gitignore)
├── settings.json        # Cấu hình bot
├── requirements.txt     # Danh sách thư viện
├── .gitignore
│
├── ui.py                # Menu chính
├── lanhdia.py           # Menu JJK style + Info
├── entertainment.py     # Giải trí / Economy
├── music.py             # Nhạc
├── raid.py              # War / Spam
├── tienich.py           # Tiện ích
├── quanly.py            # Quản lý
├── troll.py             # Troll
│
├── rate_utils.py        # Xử lý rate limit
├── cache.py             # Cache
│
├── ngon.txt             # Nội dung .thuong
├── nhay.txt             # Nội dung .lienke
├── music/               # Nhạc có sẵn
└── music_cache/         # Cache nhạc
```

---

## 📜 Bản quyền và điều khoản sử dụng

### Giấy phép MIT

```
MIT License

Copyright (c) 2026 vVnK-wh0i4m

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Điều khoản sử dụng

**1. Mục đích sử dụng:**

| ✅ Được phép | ❌ Không được phép |
|-------------|-------------------|
| Giải trí cá nhân | Quấy rối người khác |
| Nghiên cứu, học tập | Spam, gây phiền |
| Thử nghiệm tính năng | Vi phạm pháp luật |
| Quản lý server cá nhân | Gian lận, lừa đảo |

**2. Trách nhiệm người dùng:**

- Người dùng **chịu toàn bộ trách nhiệm** khi sử dụng bot.
- **PHẢI** dùng tài khoản phụ, **KHÔNG** dùng tài khoản chính.
- Người dùng phải **tuân thủ ToS của Discord**.
- Người dùng **tự chịu rủi ro** khi sử dụng self bot.

**3. Hành vi bị cấm:**

- ❌ Sử dụng bot để **quấy rối, spam** người dùng khác.
- ❌ Sử dụng bot để **vi phạm pháp luật** hoặc ToS Discord.
- ❌ **Chia sẻ token** của người dùng khác.
- ❌ Sử dụng bot cho mục đích **gian lận, lừa đảo**.

**4. Giới hạn trách nhiệm:**

- ❌ **Không đảm bảo** bot hoạt động liên tục, không lỗi.
- ❌ **Không chịu trách nhiệm** về mất mát dữ liệu.
- ❌ **Không chịu trách nhiệm** về tài khoản bị khóa.

**5. Bảo mật token:**

> ⚠️ Token cho phép truy cập **hoàn toàn** vào tài khoản Discord.

- **KHÔNG** chia sẻ token với bất kỳ ai.
- **KHÔNG** commit token lên GitHub công khai.
- **Reset ngay** nếu token bị lộ tại https://discord.com/developers/applications

---

## ❓ Câu hỏi thường gặp

### Bot cần Python version nào?

Python 3.8 trở lên. Kiểm tra: `python --version`

### Run.bat không hoạt động?

- Đảm bảo Python đã cài và nằm trong PATH
- Thử chạy thủ công: `pip install -r requirements.txt` rồi `python main.py`

### Lỗi `No module named 'discord'`?

```bash
pip install discord.py-self
```

> ⚠️ Dùng `discord.py-self`, **KHÔNG** dùng `discord.py` thường.

### Lỗi phát nhạc?

- Cần cài FFmpeg: https://ffmpeg.org/download.html
- Đặt `ffmpeg.exe` vào thư mục `music/` hoặc thêm vào PATH

### Bot không hoạt động?

Kiểm tra:
1. Token có hợp lệ không?
2. Bot có trong server không?
3. Terminal có lỗi gì không?

### Bot chạy 24/7 bằng cách nào?

Dùng hosting: Replit, Railway, VPS - xem hướng dẫn tại [self-bot-cam](https://github.com/vVnK-wh0i4m/self-bot-cam)

### Token là gì? Lấy ở đâu?

Token là chuỗi ký tự xác thực bot. Lấy bằng cách:
1. Mở Discord trên trình duyệt
2. Nhấn `F12` → Tab **Network**
3. Tìm header `Authorization`

> ⚠️ **KHÔNG** chia sẻ token. Reset tại https://discord.com/developers/applications

### Bot có an toàn không?

Self bot vi phạm ToS Discord. Sử dụng có thể bị khóa tài khoản. **Luôn dùng tài khoản phụ.**

---

<div align="center">

**⭐ Star repo nếu thấy hữu ích! ⭐**

Made with ❤️ by vVnK

</div>
