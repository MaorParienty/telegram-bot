import json
import asyncio
from telegram import *
from telegram.ext import *
from requests import *
START_ROUTES, END_ROUTES = range(2)
# Callback data
ACD, ACM, RECIEPT,\
    ABSCENT, UPDATE, ACC, AC_LIST, ACCOUNTCREATION,\
    ACCOUNTCREATION2, ACCOUNTCREATION3, ACCOUNTCREATION4,UPDATE2, \
    UPDATE3, UPDATE4,  DELETE2, START= range(16)
#ACCOUNT_DELETE, ACCOUNT_MANAGMENT, reciept, abscent, UPDATE, ACCOUNT_CREATION, ACCOUNT_LIST
fullname = ""
email = ""
phone = ""
usernameForChange = ""
index = 0
index3 = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
    [
    InlineKeyboardButton('ניהול לקוחות', callback_data=ACM),
    InlineKeyboardButton('הפקת קבלה', callback_data=RECIEPT),
    ],
    [InlineKeyboardButton('הפקת אישור היעדרות', callback_data=ABSCENT)],]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"שלום {update.effective_user.first_name}! בוא נתחיל", reply_markup=markup)
    return START_ROUTES

async def fake_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    buttons = [
    [
    InlineKeyboardButton('ניהול לקוחות', callback_data=ACM),
    InlineKeyboardButton('הפקת קבלה', callback_data=RECIEPT),
    ],
    [InlineKeyboardButton('הפקת אישור היעדרות', callback_data=ABSCENT)],]
    markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(f"שלום {update.effective_user.first_name}! בוא נתחיל", reply_markup=markup)
    return START_ROUTES

async def account_management(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""#this is one
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("יצירת לקוח חדש", callback_data=str(ACC))],
            [InlineKeyboardButton("עדכון פרטי לקוח", callback_data=str(UPDATE))],
            [InlineKeyboardButton("מחיקת לקוח", callback_data=str(ACD))
        ], [InlineKeyboardButton("רשימת משתמשים", callback_data=str(AC_LIST))],
        [InlineKeyboardButton("חזור", callback_data=str(START))],
    ]
    global index3
    index3 += 1
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="בחר באחת מהאפשרויות הבאות:", reply_markup=reply_markup
    )
    return START_ROUTES
async def delete_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    accountList = ""
    with open("customerData.json", "r+") as f:
        data = json.load(f)
        ind = 0
        for i in data:
            accountList += f"id:{ind}\nfullname: {i['fullname']}\nemail: {i['mail']}\nphone: {i['phone']}\n\n"
            ind += 1
    await query.edit_message_text(
        text=f"{accountList}  מס הסידורי של הלקוח אותו תרצה למחוק?:"
    )

    return DELETE2

async def delete_account2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    new_data = []
    with open("customerData.json", "r") as f:
        temp = json.load(f)
        data_length = len(temp)-1
        delete_option = text
        i = 0
        for entry in temp:
            if i == int(delete_option):
                pass
                i += 1
            else:
                new_data.append(entry)
                i+=1
        with open("customerData.json", "w") as f:
            json.dump(new_data, f, indent=4)
    await update.message.reply_text("נמחק ! /start בשביל לחזור למסך הבית")

async def update_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="רשום את שמך המלא"
    )
    return UPDATE2

async def update_details2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    global usernameForChange
    usernameForChange = text
    keyboard = [
        [
            InlineKeyboardButton("חזור", callback_data=str(UPDATE))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    index = 0
    with open("customerData.json", "r+") as f:
        data = json.load(f)
        for i in data:
            if usernameForChange == i["fullname"]:
                index += 1
                break
        if index == 0:
            await update.message.reply_text("שם משתמש לא קיים, אנא הזן שוב", reply_markup=reply_markup)
            return UPDATE

    await update.message.reply_text("מה תרצה לעדכון?")
    return UPDATE3

async def update_details3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    global index
    if text == "אימייל":
        index = 0
        await update.message.reply_text("הכנס את האימייל החדש")
    elif text == "שם":
        index = 1
        await update.message.reply_text("הכנס את השם החדש")
    elif text == "טלפון":
        index = 2
        await update.message.reply_text("הכנס את מס הטלפון החדש")

    return UPDATE4


async def update_details4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    global index, usernameForChange
    count = 0
    if index == 0:
        with open("customerData.json", "r+") as f:
            data = json.load(f)
            for i in data:
                if i["fullname"] == usernameForChange:
                    data[count]["mail"] = text
                count += 1
    elif index == 1:
        with open("customerData.json", "r+") as f:
            data = json.load(f)
            for i in data:
                if i["fullname"] == usernameForChange:
                    data[count]["fullname"] = text
                count += 1
    else:
        with open("customerData.json", "r+") as f:
            data = json.load(f)
            for i in data:
                if i["fullname"] == usernameForChange:
                    data[count]["phone"] = text
                count += 1
    with open('customerData.json', 'w') as file:
        json.dump(data, file, indent=4)
    await update.message.reply_text("פרטים עודכנו ! רשום /start בשביל עוד פעולות")
    return start




async def account_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("הכנס את שמך המלא:")
    return ACCOUNTCREATION

async def account_creation2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    text = update.message.text
    print(text)
    global fullname
    fullname = text
    await update.message.reply_text(
        text="הכנס אימייל:"
    )
    return ACCOUNTCREATION2


async def account_creation3(update: Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    print(text)
    global email
    email = text
    await update.message.reply_text("הכנס טלפון:")

    return ACCOUNTCREATION3

async def account_creation4(update: Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    print(text)
    global phone
    phone = text
    await update.message.reply_text("הפרטים שהזנת:")
    await update.message.reply_text("ליצור משתמש או לחזור לשנות פרטים?")
    return ACCOUNTCREATION4

async def account_creation5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    global fullname,email,phone
    if text == "צור משתמש":
        listObj = []
        # Read JSON file
        with open("customerData.json", "r+") as fp:
            listObj = json.load(fp)

        # Verify existing list
        print(listObj)
        print(type(listObj))

        listObj.append({
            "fullname": fullname,
            "mail": email,
            "phone": phone
        })

        # Verify updated list
        print(listObj)

        with open("customerData.json", 'w+') as json_file:
            json.dump(listObj, json_file,
                      indent=4,
                      separators=(',', ': '))
        await update.message.reply_text("משתמש נוצר בהצלחה!")
    else:
        return ACCOUNTCREATION


async def account_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("חזור", callback_data=str(ACM)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    accountList = ""
    with open ("customerData.json", "r+") as f:
        data = json.load(f)
        ind = 0
        for i in data:
            accountList += f"id:{ind}\nfullname: {i['fullname']}\nemail: {i['mail']}\nphone: {i['phone']}\n\n"
            ind += 1
    await query.edit_message_text(
        text=str(accountList

        ), reply_markup=reply_markup
    )
    return START_ROUTES

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return start(update, context)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7300803391:AAG7PdgiEEdiHsKKGYXZPPPtP1frJW5QXUQ").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(fake_start, pattern="^" + str(START) + "$"),
                CallbackQueryHandler(account_management, pattern="^" + str(ACM) + "$"),
                CallbackQueryHandler(delete_account, pattern="^" + str(ACD) + "$"),
                CallbackQueryHandler(update_details, pattern="^" + str(UPDATE) + "$"),
                CallbackQueryHandler(account_creation, pattern="^" + str(ACC) + "$"),
                CallbackQueryHandler(account_list, pattern="^" + str(AC_LIST) + "$"),
            ],
            ACCOUNTCREATION: [MessageHandler(filters.ALL, account_creation2)],
            ACCOUNTCREATION2: [MessageHandler(filters.ALL, account_creation3)],
            ACCOUNTCREATION3: [MessageHandler(filters.ALL, account_creation4)],
            ACCOUNTCREATION4: [MessageHandler(filters.ALL, account_creation5)],
            UPDATE2: [MessageHandler(filters.ALL, update_details2)],
            UPDATE3: [MessageHandler(filters.ALL, update_details3)],
            UPDATE4: [MessageHandler(filters.ALL, update_details4)],
            DELETE2: [MessageHandler(filters.ALL, delete_account2)],

    },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
