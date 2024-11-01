import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# Token bot dan ID owner
BOT_TOKEN = '7217510375:AAHr0T-ZKGGZPsgRgdTBKJw7lRX1Fj3S7Bg'
OWNER_ID = '5357845454'

# Load atau inisialisasi databot.json
try:
    with open('databot.json', 'r') as file:
        databot = json.load(file)
except FileNotFoundError:
    databot = {}

# Fungsi untuk mengemas kini data pengguna
def update_user_data(user):
    user_id = str(user.id)
    databot[user_id] = {
        'username': user.username,
        'full_name': user.full_name,
        'baki': databot.get(user_id, {}).get('baki', 0)
    }
    with open('databot.json', 'w') as file:
        json.dump(databot, file)

# Fungsi untuk mengira harga
def calculate_price(service_type, amount):
    price_list = {
        'tiktok_view': 1,
        'tiktok_like': 2,
        'tiktok_follower': 10.00,
        'instagram_view': 1,
        'instagram_like': 1.50,
        'instagram_follower': 5
    }
    return round(price_list[service_type] * (amount / 1000), 2)

# Fungsi untuk mengendalikan perintah /start
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update_user_data(user)
    
    # Kira baki semasa
    baki_semasa = databot[str(user.id)]['baki']
    
    # Mesej Selamat Datang
    welcome_message = f"Selamat datang {user.full_name} ke SocialMediaMax! 🚀\n" \
                      f"*BAKI ANDA : RM {baki_semasa}*\n\n" \
                      "Nak akaun media sosial anda melonjak populariti? SocialMediaMax adalah solusi terbaik untuk anda! Kami menawarkan perkhidmatan pantas dan berkualiti tinggi untuk meningkatkan follower, like, dan view di TikTok serta Instagram. Bukan itu sahaja, anda juga boleh dapatkan akaun Netflix premium untuk hiburan tanpa batas!\n\n" \
                      "Jangan biarkan akaun anda sepi, jadikan ia pusat perhatian dengan SocialMediaMax. Sama ada anda ingin mengukuhkan jenama, mempromosikan kandungan, atau sekadar meningkatkan pengaruh, kami ada cara yang sesuai untuk anda. 🌟\n\nHarga per 1k\n\nTIKTOKview: Rm1\n\nTIKTOKlike:Rm 2\n\nTIKTOKfollower:Rm 10.00\n\nINSTAGRAMview:Rm1\n\nINSTAGRAMlike: Rm1.50\n\nINSTAGRAMfollower: Rm5\n\n" \
                      "Bergabunglah dengan ribuan pengguna yang telah mempercayai SocialMediaMax untuk membawa akaun mereka ke puncak populariti. Mulakan sekarang dan lihat perbezaannya!"
    
    keyboard = [
        [InlineKeyboardButton("TAMBAH NILAI", callback_data='tambah_nilai')],
        [InlineKeyboardButton("TIKTOK", callback_data='tiktok'), InlineKeyboardButton("INSTAGRAM", callback_data='instagram')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

# Fungsi untuk mengendalikan callback dari butang
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user_id = str(query.from_user.id)
    full_name = databot[user_id]['full_name']
    username = databot[user_id]['username']
    
    if query.data == 'tambah_nilai':
        no_transaksi = str(random.randint(100000, 999999))
        notif_owner = f"{full_name} ingin tambah nilai\n" \
                      f"No Transaksi: {no_transaksi}\n" \
                      f"ID : {user_id}\n" \
                      f"Username:@{username}"
        
        notif_user = f"{full_name} sila Transfer duit ke salah satu akaun di bawah\n\n" \
                     "Nama penerima:\n\n" \
                     "MUHAMMAD FADHIL BIN ZULKIFLI\n\n" \
                     "CIMB: 7639980582\n" \
                     "TNG: 601173139757\n" \
                     "DuitNow: 131579421219\n\n" \
                     "Transfer sesuai yang mau diisi. Ref letak no transaksi. Min RM10.\n" \
                     f"No Transaksi: {no_transaksi}\n" \
                     "Sila Transfer ke akaun diatas dan isikan no Transaksi di bahagian reff. Dan kirim Resit  ke bot ini."
        
        context.bot.send_message(chat_id=OWNER_ID, text=notif_owner)
        query.message.reply_text(notif_user)
    
    elif query.data == 'tiktok' or query.data == 'instagram':
        query.message.delete()
        general_note = "📝General Note:\n" \
                       "✅There can be changes in the mentioned features during updation times\n" \
                       "✅Make Sure Your Accounts Are Public Before Making Your Order\n" \
                       "0-3% percent drop\n\n" \
                       "PILIH SERVICE:"
        
        keyboard = [
            [InlineKeyboardButton("LIKE", callback_data=f'{query.data}_like')],
            [InlineKeyboardButton("VIEW", callback_data=f'{query.data}_view')],
            [InlineKeyboardButton("FOLLOWER", callback_data=f'{query.data}_follower')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.message.reply_text(general_note, reply_markup=reply_markup)
    
    elif 'like' in query.data or 'view' in query.data or 'follower' in query.data:
        service_type = query.data.replace('_', ' ')
        query.message.reply_text(f"Masukkan jumlah {service_type} yang ingin dibeli:")
        context.user_data['service_type'] = query.data
    
    elif query.data == 'ok':
        service_type = context.user_data['service_type']
        amount = context.user_data['amount']
        total_price = calculate_price(service_type, amount)
        
        if databot[user_id]['baki'] < total_price:
            query.message.reply_text("Baki tidak mencukupi. Pembelian dibatalkan.")
        else:
            no_transaksi = str(random.randint(100000, 999999))
            notif_owner = f"No Transaksi: {no_transaksi}\n" \
                          f"Jenis: {service_type.split('_')[1].capitalize()}\n" \
                          f"SocialApp: {service_type.split('_')[0].capitalize()}\n" \
                          f"Jumlah: {amount}\n" \
                          f"ID: {user_id}\n" \
                          f"Harga: RM{total_price}\n" \
                          f"Username: @{username}"
            
            context.bot.send_message(chat_id=OWNER_ID, text=notif_owner)
            query.message.reply_text("Pembelian berjaya. Sila Kirim Link ke @earlxz atau https://wa.link/s5yhf4 untuk pemprosesan.")
            databot[user_id]['baki'] -= total_price
            with open('databot.json', 'w') as file:
                json.dump(databot, file)
    
def process_message(update: Update, context: CallbackContext):
    try:
        amount = int(update.message.text)
        service_type = context.user_data['service_type']
        total_price = calculate_price(service_type, amount)
        
        if amount < 1000:
            update.message.reply_text("Minimum pembelian adalah 1k. Sila cuba lagi.")
        else:
            context.user_data['amount'] = amount
            update.message.reply_text(f"Harga: RM{total_price}\nJika nak batalkan tekan /start semula.",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("OK", callback_data='ok')]]))
    except ValueError:
        update.message.reply_text("Sila masukkan jumlah yang sah.")

def add_balance(update: Update, context: CallbackContext):
    if str(update.message.from_user.id) == OWNER_ID:
        try:
            user_id = context.args[0]
            amount = float(context.args[1])
            databot[user_id]['baki'] += amount
            with open('databot.json', 'w') as file:
                json.dump(databot, file)
            context.bot.send_message(chat_id=user_id, text=f"Baki anda telah ditambah sebanyak RM{amount}.")
            update.message.reply_text(f"Tambah nilai berjaya untuk ID {user_id}.")
        except (IndexError, ValueError):
            update.message.reply_text("Penggunaan: /add {user_id} {jumlah}")
    else:
        update.message.reply_text("Anda tidak mempunyai akses untuk perintah ini.")

def subtract_balance(update: Update, context: CallbackContext):
    if str(update.message.from_user.id) == OWNER_ID:
        try:
            user_id = context.args[0]
            amount = float(context.args[1])
            databot[user_id]['baki'] -= amount
            with open('databot.json', 'w') as file:
                json.dump(databot, file)
            context.bot.send_message(chat_id=user_id, text=f"Baki anda telah ditolak sebanyak RM{amount}.")
            update.message.reply_text(f"Tolak nilai berjaya untuk ID {user_id}.")
        except (IndexError, ValueError):
            update.message.reply_text("Penggunaan: /tolak {user_id} {jumlah}")
    else:
        update.message.reply_text("Anda tidak mempunyai akses untuk perintah ini.")

def broadcast(update: Update, context: CallbackContext):
    if str(update.message.from_user.id) == OWNER_ID and update.message.reply_to_message:
        content = update.message.reply_to_message
        sent = 0
        failed = 0
        
        for user_id in databot:
            try:
                context.bot.copy_message(chat_id=user_id, from_chat_id=OWNER_ID, message_id=content.message_id)
                sent += 1
            except:
                failed += 1
        
        update.message.reply_text(f"Broadcast selesai. Berjaya: {sent}, Gagal: {failed}")
    else:
        update.message.reply_text("Anda tidak mempunyai akses atau tiada mesej yang direply untuk broadcast.")

def forward_to_owner(update: Update, context: CallbackContext):
    if str(update.message.from_user.id) != OWNER_ID:
        context.bot.forward_message(chat_id=OWNER_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

def reply_to_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.reply_to_message.forward_from:
        target_user_id = update.message.reply_to_message.forward_from.id
        context.bot.copy_message(chat_id=target_user_id, from_chat_id=OWNER_ID, message_id=update.message.message_id)

# Fungsi utama untuk menjalankan bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('add', add_balance))
    dp.add_handler(CommandHandler('tolak', subtract_balance))
    dp.add_handler(CommandHandler('broadcast', broadcast))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))
    dp.add_handler(MessageHandler(Filters.all, forward_to_owner))
    dp.add_handler(MessageHandler(Filters.reply & Filters.user(user_id=int(OWNER_ID)), reply_to_user))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
