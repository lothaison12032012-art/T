# ==================== PHẦN 1/10: IMPORT & CONFIG ====================

import sqlite3
import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# ==================== CẤU HÌNH ====================

BOT_TOKEN = "8824465620:AAHeFXWbReAHwvkhR0gKlsSDD_dr-aaI3BM"
OWNER_ID = 8878003413

START_LINH_THACH = 100
START_HP = 20
START_LINH_LUC = 10

# ==================== DANH SÁCH TƯ CHẤT ====================

TU_CHAT_LIST = [
    {"id": "PheVat", "name": "Vô Căn", "color": "⚪", "rate": 15, "max_level": "Luyện Khí Đỉnh", "exp_per": 5, "break_rate": 5},
    {"id": "KemCoi", "name": "Trần Tục", "color": "⚫", "rate": 10, "max_level": "Luyện Khí Trung", "exp_per": 8, "break_rate": 10},
    {"id": "BinhThuong", "name": "Phàm Nhân", "color": "🟤", "rate": 10, "max_level": "Trúc Cơ Sơ", "exp_per": 12, "break_rate": 15},
    {"id": "TapDich", "name": "Linh Căn Tạp", "color": "🟢", "rate": 12, "max_level": "Trúc Cơ Hậu", "exp_per": 15, "break_rate": 20},
    {"id": "HonHop", "name": "Ngũ Hành Hỗn Hợp", "color": "🟡", "rate": 8, "max_level": "Trúc Cơ Đỉnh", "exp_per": 20, "break_rate": 25},
    {"id": "NoiMon", "name": "Tam Linh Căn", "color": "🔵", "rate": 10, "max_level": "Kết Đan Hậu", "exp_per": 25, "break_rate": 30},
    {"id": "ChanTruyen", "name": "Song Linh Căn", "color": "🟣", "rate": 8, "max_level": "Nguyên Anh Hậu", "exp_per": 35, "break_rate": 50},
    {"id": "KiemTam", "name": "Kiếm Đạo Chi Tâm", "color": "⚔️", "rate": 5, "max_level": "Nguyên Anh Đỉnh", "exp_per": 40, "break_rate": 55},
    {"id": "DanThe", "name": "Đan Đạo Chi Thể", "color": "🍃", "rate": 4, "max_level": "Nguyên Anh Đỉnh", "exp_per": 40, "break_rate": 55},
    {"id": "PhuThe", "name": "Phù Chú Chi Thể", "color": "✨", "rate": 3, "max_level": "Nguyên Anh Đỉnh", "exp_per": 40, "break_rate": 55},
    {"id": "ThienTai", "name": "Thiên Linh Căn", "color": "🟠", "rate": 4, "max_level": "Hóa Thần Hậu", "exp_per": 50, "break_rate": 70},
    {"id": "HuyetMachCo", "name": "Thái Cổ Huyết Mạch", "color": "🩸", "rate": 2, "max_level": "Hóa Thần Hậu", "exp_per": 55, "break_rate": 75},
    {"id": "ThanThe", "name": "Thần Linh Chi Thể", "color": "☀️", "rate": 2, "max_level": "Hóa Thần Hậu", "exp_per": 55, "break_rate": 75},
    {"id": "MaThe", "name": "Ma Đạo Chi Thể", "color": "🌑", "rate": 2, "max_level": "Hóa Thần Hậu", "exp_per": 55, "break_rate": 75},
    {"id": "QuaiVat", "name": "Dị Linh Căn", "color": "🔴", "rate": 2, "max_level": "Luyện Hư", "exp_per": 70, "break_rate": 85},
    {"id": "HonDonThe", "name": "Hỗn Độn Chi Thể", "color": "🌫️", "rate": 1, "max_level": "Luyện Hư", "exp_per": 75, "break_rate": 88},
    {"id": "ThaiCo", "name": "Thái Sơ Huyết Mạch", "color": "🩸", "rate": 0.8, "max_level": "Hợp Thể", "exp_per": 80, "break_rate": 90},
    {"id": "TienCan", "name": "Tiên Đạo Chi Căn", "color": "🤍", "rate": 0.5, "max_level": "Đại Thừa", "exp_per": 90, "break_rate": 92},
    {"id": "NhanVatChinh", "name": "Hỗn Độn Linh Căn", "color": "💎", "rate": 0.3, "max_level": "Độ Kiếp", "exp_per": 100, "break_rate": 95},
]

# LỌ ĐẾ - ẨN HOÀN TOÀN
LO_DE = {"id": "LoDe", "name": "Vô Thượng Đạo Căn", "color": "🌈", "rate": 0.1, "max_level": "LỌ ĐẾ", "exp_per": 999, "break_rate": 100}
# ==================== PHẦN 2/10: DATABASE ====================

DB_NAME = "game.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            gender TEXT,
            tu_chat TEXT,
            tu_chat_goc TEXT,
            canh_gioi TEXT DEFAULT 'Luyện Khí Tầng 1',
            level INTEGER DEFAULT 1,
            exp INTEGER DEFAULT 0,
            exp_need INTEGER DEFAULT 100,
            hp INTEGER DEFAULT 20,
            hp_max INTEGER DEFAULT 20,
            linh_luc INTEGER DEFAULT 10,
            linh_luc_max INTEGER DEFAULT 10,
            linh_thach INTEGER DEFAULT 0,
            vi_tri TEXT DEFAULT 'Nhân giới - Tiên Đài Vân Mộng',
            da_trung_sinh INTEGER DEFAULT 0,
            so_lan_trung_sinh INTEGER DEFAULT 0,
            tuoi_tho INTEGER DEFAULT 100,
            created_at TEXT,
            last_save TEXT,
            da_chon_gioi_tinh INTEGER DEFAULT 0,
            da_soi_tu_chat INTEGER DEFAULT 0,
            la_lo_de INTEGER DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            quantity INTEGER DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            level INTEGER DEFAULT 1,
            hp INTEGER DEFAULT 30,
            hp_max INTEGER DEFAULT 30,
            attack INTEGER DEFAULT 5,
            defense INTEGER DEFAULT 2,
            bond INTEGER DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS sects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            owner_id INTEGER,
            phe TEXT DEFAULT 'Chính đạo',
            level INTEGER DEFAULT 1,
            fund INTEGER DEFAULT 0,
            member_count INTEGER DEFAULT 1,
            created_at TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS sect_members (
            user_id INTEGER PRIMARY KEY,
            sect_id INTEGER,
            rank TEXT DEFAULT 'Thành viên',
            joined_at TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS dao_lu (
            user_id INTEGER PRIMARY KEY,
            partner_id INTEGER,
            bond INTEGER DEFAULT 50,
            since TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS trung_sinh_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            kiem_truoc TEXT,
            tu_chat_cu TEXT,
            canh_gioi_cu TEXT,
            thoi_gian TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database đã được tạo thành công!")

def create_player(user_id, username, gender):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO players (user_id, username, gender, created_at, last_save, da_chon_gioi_tinh)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, gender, now, now, 1))
    conn.commit()
    conn.close()
    return True

def get_player(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
    data = c.fetchone()
    conn.close()
    return data

def update_player(user_id, **kwargs):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for key, value in kwargs.items():
        c.execute(f'UPDATE players SET {key} = ? WHERE user_id = ?', (value, user_id))
    c.execute('UPDATE players SET last_save = ? WHERE user_id = ?', 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    conn.close()
    return True

def player_exists(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT user_id FROM players WHERE user_id = ?', (user_id,))
    data = c.fetchone()
    conn.close()
    return data is not None

def add_item(user_id, item_name, quantity=1):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?', 
              (user_id, item_name))
    result = c.fetchone()
    if result:
        new_qty = result[0] + quantity
        c.execute('UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_name = ?',
                  (new_qty, user_id, item_name))
    else:
        c.execute('INSERT INTO inventory (user_id, item_name, quantity) VALUES (?, ?, ?)',
                  (user_id, item_name, quantity))
    conn.commit()
    conn.close()
    return True

def get_inventory(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT item_name, quantity FROM inventory WHERE user_id = ?', (user_id,))
    data = c.fetchall()
    conn.close()
    return data

def add_pet(user_id, name, level=1):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO pets (user_id, name, level, hp, hp_max, attack, defense, bond)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, level, 30 + level*10, 30 + level*10, 5 + level*2, 2 + level, 0))
    conn.commit()
    conn.close()
    return True

def get_pets(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM pets WHERE user_id = ?', (user_id,))
    data = c.fetchall()
    conn.close()
    return data

def create_sect(name, owner_id, phe='Chính đạo'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO sects (name, owner_id, phe, created_at, fund)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, owner_id, phe, now, 2000))
    sect_id = c.lastrowid
    c.execute('''
        INSERT INTO sect_members (user_id, sect_id, rank, joined_at)
        VALUES (?, ?, ?, ?)
    ''', (owner_id, sect_id, 'Tông chủ', now))
    conn.commit()
    conn.close()
    return sect_id

def get_sect_by_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT s.* FROM sects s
        JOIN sect_members sm ON s.id = sm.sect_id
        WHERE sm.user_id = ?
    ''', (user_id,))
    data = c.fetchone()
    conn.close()
    return data

def set_dao_lu(user_id, partner_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT OR REPLACE INTO dao_lu (user_id, partner_id, since)
        VALUES (?, ?, ?)
    ''', (user_id, partner_id, now))
    c.execute('''
        INSERT OR REPLACE INTO dao_lu (user_id, partner_id, since)
        VALUES (?, ?, ?)
    ''', (partner_id, user_id, now))
    conn.commit()
    conn.close()
    return True

def get_dao_lu(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT partner_id FROM dao_lu WHERE user_id = ?', (user_id,))
    data = c.fetchone()
    conn.close()
    return data[0] if data else None

def add_trung_sinh_history(user_id, kiem_truoc, tu_chat_cu, canh_gioi_cu):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO trung_sinh_history (user_id, kiem_truoc, tu_chat_cu, canh_gioi_cu, thoi_gian)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, kiem_truoc, tu_chat_cu, canh_gioi_cu, now))
    conn.commit()
    conn.close()
    return True
# ==================== PHẦN 3/10: HÀM PHỤ TRỢ ====================

def get_display_name(user):
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        return user.first_name
    return "Tu sĩ vô danh"

def roll_tu_chat():
    rand = random.random() * 1000
    if rand < 1:
        return LO_DE
    elif rand < 4:
        return TU_CHAT_LIST[18]
    elif rand < 12:
        return TU_CHAT_LIST[17]
    elif rand < 20:
        return TU_CHAT_LIST[16]
    elif rand < 30:
        return TU_CHAT_LIST[15]
    elif rand < 50:
        return TU_CHAT_LIST[14]
    elif rand < 70:
        return TU_CHAT_LIST[13]
    elif rand < 90:
        return TU_CHAT_LIST[12]
    elif rand < 110:
        return TU_CHAT_LIST[11]
    elif rand < 150:
        return TU_CHAT_LIST[10]
    elif rand < 180:
        return TU_CHAT_LIST[9]
    elif rand < 220:
        return TU_CHAT_LIST[8]
    elif rand < 270:
        return TU_CHAT_LIST[7]
    elif rand < 350:
        return TU_CHAT_LIST[6]
    elif rand < 450:
        return TU_CHAT_LIST[5]
    elif rand < 530:
        return TU_CHAT_LIST[4]
    elif rand < 650:
        return TU_CHAT_LIST[3]
    elif rand < 750:
        return TU_CHAT_LIST[2]
    elif rand < 850:
        return TU_CHAT_LIST[1]
    else:
        return TU_CHAT_LIST[0]

def get_canh_gioi(level):
    if level <= 12:
        return f"Luyện Khí Tầng {level}"
    elif level <= 15:
        return f"Trúc Cơ {['Sơ', 'Trung', 'Hậu'][level-13]}"
    elif level <= 18:
        return f"Kết Đan {['Sơ', 'Trung', 'Hậu'][level-16]}"
    elif level <= 21:
        return f"Nguyên Anh {['Sơ', 'Trung', 'Hậu'][level-19]}"
    elif level <= 24:
        return f"Hóa Thần {['Sơ', 'Trung', 'Hậu'][level-22]}"
    elif level <= 27:
        return f"Luyện Hư {['Sơ', 'Trung', 'Hậu'][level-25]}"
    elif level <= 30:
        return f"Hợp Thể {['Sơ', 'Trung', 'Hậu'][level-28]}"
    elif level <= 33:
        return f"Đại Thừa {['Sơ', 'Trung', 'Hậu'][level-31]}"
    else:
        return f"Độ Kiếp (Đạo {level-33})"
# ==================== PHẦN 4/10: MENU CHÍNH ====================

def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("⚔️ Tu luyện", callback_data="menu_train"),
        InlineKeyboardButton("🎯 Nhiệm vụ", callback_data="menu_quest"),
        InlineKeyboardButton("🗺️ Di chuyển", callback_data="menu_move"),
        InlineKeyboardButton("🎒 Túi đồ", callback_data="menu_inventory"),
        InlineKeyboardButton("🏪 Chợ", callback_data="menu_shop"),
        InlineKeyboardButton("👥 Chiến đấu", callback_data="menu_fight"),
        InlineKeyboardButton("🐾 Linh thú", callback_data="menu_pet"),
        InlineKeyboardButton("💑 Đạo lữ", callback_data="menu_dao_lu"),
        InlineKeyboardButton("🔧 Trạng thái", callback_data="menu_status"),
        InlineKeyboardButton("🏛️ Lập tông", callback_data="menu_sect"),
        InlineKeyboardButton("📜 Nhật ký", callback_data="menu_diary"),
        InlineKeyboardButton("🎖️ Huy chương", callback_data="menu_achievement"),
        InlineKeyboardButton("🌙 Nghỉ ngơi", callback_data="menu_rest"),
        InlineKeyboardButton("🗺️ Vạn giới đồ", callback_data="menu_map"),
    )
    return keyboard

async def show_main_menu(message, user_id):
    player = get_player(user_id)
    if not player:
        await message.answer("❌ Bạn chưa có nhân vật! Hãy dùng /start để tạo.")
        return
    
    is_lo_de = player[22] == 1
    
    text = f"🧙 {player[1]} - {player[4]}\n"
    text += f"{player[2]} Giới tính: {player[2]}\n"
    text += f"🏠 Thân phận: TÁN TU\n"
    text += "-" * 40 + "\n"
    text += f"❤️ HP: {player[7]}/{player[8]}\n"
    text += f"⚡ Linh lực: {player[9]}/{player[10]}\n"
    text += f"📊 EXP: {player[6]}/{player[11]}\n"
    text += f"💰 Linh thạch: {player[12]} Hạ\n"
    text += f"📍 Vị trí: {player[13]}\n"
    text += "-" * 40 + "\n"
    text += "📢 Hệ thống: Tu luyện chăm chỉ để đạt Kết Đan!\n"
    text += "💾 Game tự động lưu sau mỗi hành động!\n"
    
    if is_lo_de:
        text += "🐿️🍶 Bạn là Lọ Đế! Vô địch tuyệt đối!\n"
    
    await message.answer(text, reply_markup=main_menu_keyboard())
# ==================== PHẦN 5/10: /START & SOI TƯ CHẤT ====================

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user = message.from_user
    user_id = user.id
    display_name = get_display_name(user)
    
    if player_exists(user_id):
        await show_main_menu(message, user_id)
        return
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🧑 Nam", callback_data="gender_nam"),
        InlineKeyboardButton("👩 Nữ", callback_data="gender_nu")
    )
    
    await message.answer(
        f"🌌 CHÀO MỪNG {display_name} ĐẾN VỚI THẾ GIỚI TU TIÊN!\n"
        f"-" * 40 + "\n"
        f"🔰 BẠN LÀ MỘT PHÀM NHÂN!\n"
        f"   Chưa biết gì về tu tiên.\n"
        f"   Chưa thuộc tông môn nào.\n"
        f"   Chưa có Linh thạch.\n\n"
        f"📜 TRƯỚC KHI BẮT ĐẦU, HÃY CHỌN GIỚI TÍNH!\n\n"
        f"⚠️ LƯU Ý: Giới tính KHÔNG THỂ ĐỔI sau khi chọn!",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data.startswith('gender_'))
async def handle_gender(callback: types.CallbackQuery):
    user = callback.from_user
    user_id = user.id
    gender = "Nam" if callback.data == "gender_nam" else "Nữ"
    
    create_player(user_id, get_display_name(user), gender)
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔮 SOI TƯ CHẤT NGAY!", callback_data="soi_tu_chat"))
    
    await callback.message.edit_text(
        f"✅ ĐÃ CHỌN GIỚI TÍNH: {gender}\n"
        f"-" * 40 + "\n"
        f"👤 {get_display_name(user)}\n"
        f"📅 Ngày tạo: {datetime.now().strftime('%d/%m/%Y')}\n\n"
        f"📜 TIẾP THEO: HÃY ĐẾN BÀN SOI LINH CĂN!\n\n"
        f"💰 Chi phí: MIỄN PHÍ!\n"
        f"📊 Lần soi: Đầu tiên và duy nhất!",
        reply_markup=keyboard
    )
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == 'soi_tu_chat')
async def handle_soi_tu_chat(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    player = get_player(user_id)
    
    if not player:
        await callback.answer("❌ Chưa có nhân vật!")
        return
    
    if player[20] == 1:
        await callback.answer("❌ Bạn đã soi tư chất rồi!")
        return
    
    tu_chat = roll_tu_chat()
    is_lo_de = tu_chat["id"] == "LoDe"
    
    update_player(user_id, 
                  tu_chat=tu_chat["name"],
                  tu_chat_goc=tu_chat["name"],
                  da_soi_tu_chat=1,
                  la_lo_de=1 if is_lo_de else 0)
    
    text = f"🔮 BÀN SOI LINH CĂN - TIÊN ĐÀI VÂN MỘNG\n"
    text += "-" * 40 + "\n"
    text += f"💥 KẾT QUẢ: {tu_chat['color']} {tu_chat['name']} {tu_chat['color']}\n\n"
    text += f"📊 Tư chất: {tu_chat['name']}\n"
    text += f"📈 Tiềm năng tối đa: {tu_chat['max_level']}\n"
    text += f"⚡ EXP/lần đả tọa: {tu_chat['exp_per']}\n"
    text += f"🎯 Xác suất đột phá: {tu_chat['break_rate']}%\n"
    
    if is_lo_de:
        text += "\n🐿️🍶 CHÚC MỪNG! BẠN LÀ LỌ ĐẾ!\n"
        text += "🌈 Vô địch tuyệt đối!\n"
    
    await callback.message.edit_text(text)
    await callback.answer()
# ==================== PHẦN 6/10: MENU CALLBACK ====================

@dp.callback_query_handler(lambda c: c.data == 'menu_train')
async def menu_train(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    player = get_player(user_id)
    if not player:
        await callback.answer("❌ Chưa có nhân vật!")
        return
    
    tu_chat = roll_tu_chat()
    text = f"⚔️ TU LUYỆN - {player[1]}\n"
    text += "-" * 40 + "\n"
    text += f"📊 Cảnh giới: {player[4]}\n"
    text += f"📊 EXP: {player[6]}/{player[11]}\n"
    text += f"⚡ Linh lực: {player[9]}/{player[10]}\n"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🧘 Đả tọa", callback_data="train"),
        InlineKeyboardButton("💊 Dùng đan", callback_data="train_dan"),
        InlineKeyboardButton("⚡ Đột phá", callback_data="breakthrough"),
        InlineKeyboardButton("🔙 Quay lại", callback_data="back_to_main")
    )
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == 'train')
async def do_train(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    player = get_player(user_id)
    
    tu_chat = roll_tu_chat()
    exp_gain = tu_chat['exp_per']
    linh_luc_gain = 5
    
    if player[9] < 5:
        await callback.answer("❌ Không đủ Linh lực! Hãy nghỉ ngơi!")
        return
    
    new_exp = player[6] + exp_gain
    new_linh_luc = player[9] - 5
    new_hp = min(player[7] + 5, player[8])
    
    update_player(user_id, exp=new_exp, linh_luc=new_linh_luc, hp=new_hp)
    
    text = f"🧘 ĐANG ĐẢ TỌA - {player[1]}\n"
    text += "-" * 40 + "\n"
    text += f"📈 EXP: {player[6]} → {new_exp}\n"
    text += f"⚡ Linh lực: {player[9]} → {new_linh_luc}\n"
    text += f"❤️ HP: {player[7]} → {new_hp}\n"
    
    if new_exp >= player[11]:
        new_level = player[5] + 1
        new_exp_need = player[11] + 50
        new_hp_max = player[8] + 10
        new_linh_luc_max = player[10] + 5
        
        update_player(user_id, 
                      level=new_level, 
                      exp=new_exp - player[11], 
                      exp_need=new_exp_need,
                      hp_max=new_hp_max,
                      linh_luc_max=new_linh_luc_max)
        
        text += f"\n🎉 LÊN CẤP! {get_canh_gioi(new_level)}!"
        text += f"\n❤️ HP max: +10\n⚡ Linh lực max: +5"
    
    text += f"\n💾 ĐÃ TỰ ĐỘNG LƯU!"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🧘 Đả tọa tiếp", callback_data="train"),
        InlineKeyboardButton("🔙 Quay lại", callback_data="menu_train")
    )
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == 'back_to_main')
async def back_to_main(callback: types.CallbackQuery):
    await show_main_menu(callback.message, callback.from_user.id)
    await callback.answer()
# ==================== PHẦN 7/10: TRẠNG THÁI ====================

@dp.callback_query_handler(lambda c: c.data == 'menu_status')
async def menu_status(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    player = get_player(user_id)
    if not player:
        await callback.answer("❌ Chưa có nhân vật!")
        return
    
    tu_chat = roll_tu_chat()
    
    text = f"🔧 HỒ SƠ - {player[1]}\n"
    text += "-" * 40 + "\n"
    text += f"👤 Tên: {player[1]}\n"
    text += f"{player[2]} Giới tính: {player[2]}\n"
    text += f"📊 Cảnh giới: {player[4]}\n"
    text += f"🟣 Tư chất: {player[3]}\n"
    text += f"📈 EXP: {player[6]}/{player[11]}\n"
    text += f"❤️ HP: {player[7]}/{player[8]}\n"
    text += f"⚡ Linh lực: {player[9]}/{player[10]}\n"
    text += f"💰 Linh thạch: {player[12]} Hạ\n"
    text += f"📍 Vị trí: {player[13]}\n"
    text += f"📅 Ngày tạo: {player[18]}\n"
    text += f"🔄 Đã trùng sinh: {'✅' if player[15] == 1 else '❌'}\n"
    text += f"📊 Số lần trùng sinh: {player[16]}\n"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔙 Quay lại", callback_data="back_to_main")
    )
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
# ==================== PHẦN 8/10: LỆNH /HELP ====================

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    text = "📋 DANH SÁCH LỆNH - THẾ GIỚI TU TIÊN\n"
    text += "-" * 40 + "\n\n"
    text += "🔰 LỆNH CƠ BẢN:\n"
    text += "/start - Bắt đầu game\n"
    text += "/menu - Menu chính\n"
    text += "/help - Xem hướng dẫn\n\n"
    text += "⚔️ TU LUYỆN:\n"
    text += "/train - Đả tọa tu luyện\n"
    text += "/breakthrough - Đột phá cảnh giới\n\n"
    text += "🎯 NHIỆM VỤ:\n"
    text += "/quest - Xem nhiệm vụ\n\n"
    text += "🗺️ DI CHUYỂN:\n"
    text += "/map - Xem bản đồ\n"
    text += "/move [tên] - Di chuyển\n\n"
    text += "🐾 LINH THÚ:\n"
    text += "/pet - Xem Linh thú\n"
    text += "/pet_find - Tìm Linh thú\n\n"
    text += "💑 ĐẠO LỮ:\n"
    text += "/dao_lu - Xem đạo lữ\n"
    text += "/dao_lu_ket @user - Kết đạo lữ\n\n"
    text += "🔧 ADMIN:\n"
    text += "/set_tu_chat @user [tư_chất] - Set tư chất\n"
    text += "/set_phe_vat @user - Set Phế vật\n"
    text += "/view_player @user - Xem người chơi\n"
    
    await message.answer(text)

@dp.message_handler(commands=['menu'])
async def cmd_menu(message: types.Message):
    await show_main_menu(message, message.from_user.id)
# ==================== PHẦN 9/10: LỆNH ADMIN ====================

@dp.message_handler(commands=['set_tu_chat'])
async def cmd_set_tu_chat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id != OWNER_ID:
        await message.answer("❌ Bạn không có quyền sử dụng lệnh này!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Cú pháp: /set_tu_chat @user [tư_chất]")
        return
    
    target = args[1].replace('@', '')
    tu_chat_name = args[2]
    
    # Tìm user_id từ username
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT user_id FROM players WHERE username LIKE ?', (f'@{target}%',))
    result = c.fetchone()
    conn.close()
    
    if not result:
        await message.answer(f"❌ Không tìm thấy người chơi @{target}!")
        return
    
    target_id = result[0]
    
    # Tìm tư chất
    tu_chat = None
    for tc in TU_CHAT_LIST:
        if tc["id"].lower() == tu_chat_name.lower():
            tu_chat = tc
            break
    
    if tu_chat is None:
        await message.answer("❌ Tư chất không hợp lệ!")
        return
    
    old_player = get_player(target_id)
    old_tu_chat = old_player[3]
    
    update_player(target_id, tu_chat=tu_chat["name"], tu_chat_goc=old_tu_chat)
    
    await message.answer(
        f"✅ SET TƯ CHẤT THÀNH CÔNG!\n"
        f"👤 {target}\n"
        f"📊 Tư chất cũ: {old_tu_chat}\n"
        f"📊 Tư chất mới: {tu_chat['color']} {tu_chat['name']}"
    )

@dp.message_handler(commands=['view_player'])
async def cmd_view_player(message: types.Message):
    user_id = message.from_user.id
    
    if user_id != OWNER_ID:
        await message.answer("❌ Bạn không có quyền sử dụng lệnh này!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Cú pháp: /view_player @user")
        return
    
    target = args[1].replace('@', '')
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT user_id FROM players WHERE username LIKE ?', (f'@{target}%',))
    result = c.fetchone()
    conn.close()
    
    if not result:
        await message.answer(f"❌ Không tìm thấy người chơi @{target}!")
        return
    
    target_id = result[0]
    player = get_player(target_id)
    
    if not player:
        await message.answer(f"❌ Người chơi @{target} chưa có nhân vật!")
        return
    
    text = f"👤 XEM NGƯỜI CHƠI - @{target}\n"
    text += "-" * 40 + "\n"
    text += f"📊 Cảnh giới: {player[4]}\n"
    text += f"🟣 Tư chất: {player[3]}\n"
    text += f"❤️ HP: {player[7]}/{player[8]}\n"
    text += f"⚡ Linh lực: {player[9]}/{player[10]}\n"
    text += f"💰 Linh thạch: {player[12]} Hạ\n"
    text += f"🔄 Đã trùng sinh: {'✅' if player[15] == 1 else '❌'}\n"
    text += f"📊 Số lần trùng sinh: {player[16]}\n"
    
    await message.answer(text)
# ==================== PHẦN 10/10: CHẠY BOT ====================

# Khởi tạo bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# ==================== CHẠY BOT ====================

if __name__ == "__main__":
    init_db()
    print("🤖 Bot đang chạy...")
    executor.start_polling(dp, skip_updates=True)