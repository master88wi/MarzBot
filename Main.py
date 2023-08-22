from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import mysql.connector
import datetime
import Marzban
# Variable
token = "**TOKEN**"
UserIdAdmin = "5522424631"
usernamedb = "root"
passworddb = "root"


# database

dbmirzapanel = mysql.connector.connect(
    host="localhost",
    user=usernamedb,
    password=passworddb
)


# CREATE DataBase
databasesql = dbmirzapanel.cursor()
databasesql.execute("SHOW DATABASES")
databases = [db[0] for db in databasesql]
if "mirzapanel" not in databases:
    databasesql.execute("CREATE DATABASE mirzapanel")
    print("Database 'mirzapanel' created.")
dbmirzapanel = mysql.connector.connect(
    host="localhost",
    user=usernamedb,
    password=passworddb,
    database="mirzapanel"
)
dbmirzapanelsql = dbmirzapanel.cursor()
dbmirzapanelsql.execute("SHOW TABLES")
CheckTables = [db[0] for db in dbmirzapanelsql]
if "users" not in CheckTables:
    dbmirzapanelsql.execute(
        "CREATE TABLE users (id INT(100), username VARCHAR(255),step VARCHAR(1000),RegistrationDate TIMESTAMP,Processing_value VARCHAR(500),User_Status VARCHAR(200))")
    print("Table \"users\" Create")
if "admins" not in CheckTables:
    dbmirzapanelsql.execute(
        "CREATE TABLE admins (id INT AUTO_INCREMENT PRIMARY KEY, id_admin VARCHAR(500))")
    print("Table \"admins\" Create")
    dbmirzapanelsql.execute(
        f"INSERT IGNORE INTO admins (id_admin) VALUES ({UserIdAdmin})")
    dbmirzapanel.commit()
if "panel" not in CheckTables:
    dbmirzapanelsql.execute(
        "CREATE TABLE panel (id INT AUTO_INCREMENT PRIMARY KEY, NamePanel VARCHAR(600), UrlPanel VARCHAR(600),Username VARCHAR(600) , password VARCHAR(700))")
    print("Table \"panel\" Create")


# connect to telegram

bot = Client(
    name="Bot Telegram Marzban",
    api_id=25996039,
    api_hash="251e185b1f0b1fdf9de875c28f70b4d2",
    bot_token=token
)

# keyboard bot
keyboard = ReplyKeyboardMarkup([
    [("👤 پروفایل")]
],
    resize_keyboard=True)
keyboardAdmin = ReplyKeyboardMarkup([
    [("🖥 پنل مرزبان")]
],
    resize_keyboard=True)
BackAdmin = ReplyKeyboardMarkup([
    [("🏠")]
],
    resize_keyboard=True)
# send message start


@bot.on_message(filters.command("start"))
def sendstart(client, message):
    bot.send_message(
        message.chat.id, "👋 سلام به ربات ما خوش آمدید", reply_markup=keyboard)

# Response text


@bot.on_message(filters.text)
def botmessage(client, message):
    # Add User To Database
    insert_query = "INSERT IGNORE INTO users (id, username, step, RegistrationDate, Processing_value, User_Status) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_values = (message.chat.id, message.chat.username,
                     'none', datetime.datetime.now(), 'none', 'Active')
    dbmirzapanelsql.execute(insert_query, insert_values)
    dbmirzapanel.commit()
    select_query = "SELECT * FROM users WHERE id = %s"
    select_values = (message.chat.id,)
    dbmirzapanelsql.execute(select_query, select_values)
    UserData = dbmirzapanelsql.fetchall()
    # Send Message To Text Profile
    if message.text == "👤 پروفایل":
        textinfo = f"👨🏻‍💻 وضعیت حساب کاربری شما:\n\n👤 نام: {message.chat.first_name}\n🕴🏻 شناسه کاربری : <code>{message.chat.id}</code>"
        bot.send_message(message.chat.id, textinfo)

    # Section Admin
    CheckAdmin = dbmirzapanelsql.execute("SELECT id_admin FROM admins")
    if f"{message.chat.id}" in [i[0].strip() for i in dbmirzapanelsql.fetchall()]:
        CommandAdmin = ["panel", "/panel",
                        "ادمین", "مدیریت", "admin", "manage"]
        if message.text in CommandAdmin:
            textwelcome = f"به پنل مدیریت خوش آمدید برای مدیریت ربات یکی از گزینه های زیر را انتخاب کنید"
            bot.send_message(message.chat.id, textwelcome,
                             reply_markup=keyboardAdmin)
        if message.text == "🏠":
            bot.send_message(
                message.chat.id,
                "🏠 به منوی مدیریت بازگشتید!",
                reply_markup=keyboardAdmin)
            dbmirzapanelsql.execute(
                f"UPDATE users SET step = 'none' WHERE id = '{message.chat.id}'")
            dbmirzapanel.commit()
            return False

        # Add Panel Marzban
        if message.text == "🖥 پنل مرزبان":
            global UrlPanel, NamePanel, UsernamePanel
            bot.send_message(
                message.chat.id,
                "⭕️ برای اضافه کردن پنل ابتدا نام پنل خود را ارسال کنید",
                reply_markup=BackAdmin)
            dbmirzapanelsql.execute(
                f"UPDATE users SET step = 'GetUrlPanel' WHERE id = '{message.chat.id}'")
            dbmirzapanel.commit()
        if UserData[0][2] == "GetUrlPanel":
            global NamePanel
            NamePanel = message.text
            bot.send_message(
                message.chat.id,
                "✅ نام پنل دریافت شد حالا آدرس پنل را ارسال کنید",
                reply_markup=BackAdmin)
            dbmirzapanelsql.execute(
                f"UPDATE users SET step = 'GetUsernamePanel' WHERE id = '{message.chat.id}'")
            dbmirzapanel.commit()
        if UserData[0][2] == "GetUsernamePanel":
            UrlPanel = message.text
            bot.send_message(
                message.chat.id,
                "✅ آدرس پنل دریافت شد حالا نام کاربری پنل را ارسال کنید",
                reply_markup=BackAdmin)
            dbmirzapanelsql.execute(
                f"UPDATE users SET step = 'GetpasswordPanel' WHERE id = '{message.chat.id}'")
            dbmirzapanel.commit()
        if UserData[0][2] == "GetpasswordPanel":
            UsernamePanel = message.text
            bot.send_message(
                message.chat.id,
                "✅ نام کاربری دریافت شد حالا رمز پنل را ارسال کنید",
                reply_markup=BackAdmin)
            dbmirzapanelsql.execute(
                f"UPDATE users SET step = 'EndStepAddPanel' WHERE id = '{message.chat.id}'")
            dbmirzapanel.commit()
        if UserData[0][2] == "EndStepAddPanel":
            CheckConect = Marzban.get_access_token(
                UrlPanel, UsernamePanel, message.text)
            if CheckConect == "Incorrect username or password":
                bot.send_message(
                    message.chat.id,
                    "😔ورود به پنل انجام نشد\n\nدلیل :  نام کاربری یا رمز عبور غلط می باشد",
                    reply_markup=keyboardAdmin)
            elif CheckConect == "Failed to connect Panel":
                bot.send_message(
                    message.chat.id,
                    "ارتباط با سرور پنل برقرار نشد",
                    reply_markup=keyboardAdmin)
            elif CheckConect.get('access_token'):
                bot.send_message(
                    message.chat.id,
                    "✅ پنل با موفقیت اضافه گردید",
                    reply_markup=keyboardAdmin)
                insert_query = "INSERT IGNORE INTO panel (NamePanel, UrlPanel, Username, Password) VALUES (%s, %s, %s, %s)"
                insert_values = (NamePanel, UrlPanel,
                                 UsernamePanel, message.text)
                dbmirzapanelsql.execute(insert_query, insert_values)
                dbmirzapanel.commit()
            dbmirzapanelsql.execute(
                f"UPDATE users SET step = 'none' WHERE id = '{message.chat.id}'")
            dbmirzapanel.commit()


bot.run()
dbmirzapanel.close()

# end
