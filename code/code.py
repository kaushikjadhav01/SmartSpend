#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import re
import os
import telebot
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()

api_token = os.getenv('TELEGRAM_BOT_TOKEN')

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

#global variables to store user choice, user list, spend categories, etc
option = {}
user_list = {}
spend_categories = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
spend_display_option = ['Day', 'Month']

#set of implemented commands and their description
commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'display': 'Show sum of expenditure for the current day/month',
    'history': 'Display spending history',
    'delete': 'Clear/Erase all your records',
    'edit': 'Edit/Change spending details'
}

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

#Define listener for requests by user
def listener(user_requests):
	for req in user_requests:
		if(req.content_type=='text'):
			print("{} name:{} chat_id:{} \nmessage: {}\n".format(str(datetime.now()),str(req.chat.first_name),str(req.chat.id),str(req.text)))


bot.set_update_listener(listener)

#defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    read_json()
    global user_list
    chat_id = m.chat.id

    text_intro = "Welcome to TrackMyDollar - a simple solution to track your expenses! \nHere is a list of available commands, please enter a command of your choice so that I can assist you further: \n\n"
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True

#defines how the /new command has to be handled/processed
@bot.message_handler(commands=['add'])
def command_add(message):
    read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in spend_categories:
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection)

def post_category_selection(message):
        try:
            chat_id = message.chat.id
            selected_category = message.text
            if not selected_category in spend_categories:
                msg = bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
                raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))

            option[chat_id] = selected_category
            message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only)'.format(str(option[chat_id])))
            bot.register_next_step_handler(message, post_amount_input)
        except Exception as e:
            bot.reply_to(message, 'Oh no! ' + str(e))
            display_text = ""
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                display_text += "/" + c + ": "
                display_text += commands[c] + "\n"
            bot.send_message(chat_id, 'Please select a menu option from below:')
            bot.send_message(chat_id, display_text)

def post_amount_input(message):
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = datetime.today().strftime(dateFormat + ' ' + timeFormat)
        date_str, category_str, amount_str = str(date_of_entry), str(option[chat_id]), str(amount_value)
        write_json(add_user_record(chat_id, "{},{},{}".format(date_str, category_str, amount_str)))
        bot.send_message(chat_id, 'The following expenditure has been recorded: You have spent ${} for {} on {}'.format(amount_str, category_str, date_str))

    except Exception as e:
        bot.reply_to(message, 'Oh no. ' + str(e))

def validate_entered_amount(amount_entered):
    if len(amount_entered) > 0 and len(amount_entered) <= 15:
        if amount_entered.isdigit:
            if re.match("^[0-9]*\\.?[0-9]*$", amount_entered):
                amount = round(float(amount_entered), 2)
                if amount > 0:
                    return str(amount)
    return 0

def write_json(user_list):
    try:
        with open('expense_record.json', 'w') as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('Sorry, the data file could not be found.')

def add_user_record(chat_id, record_to_be_added):
    global user_list
    if not (str(chat_id) in user_list):
        user_list[str(chat_id)] = []

    user_list[str(chat_id)].append(record_to_be_added)
    return user_list

#function to load .json expense record data
def read_json():
	global user_list
	try:
		if os.stat('expense_record.json').st_size!=0:
			with open('expense_record.json') as expense_record:
				expense_record_data = json.load(expense_record)
			user_list = expense_record_data

	except FileNotFoundError:
		print("---------NO RECORDS FOUND---------")


#function to fetch expenditure history of the user
@bot.message_handler(commands=['history'])
def show_history(message):
	try:
		read_json()
		chat_id=message.chat.id
		user_history=getUserHistory(chat_id)
		spend_total_str = ""
		if user_history is None:
			raise Exception("Sorry! No spending records found!")
		spend_history_str = "Here is your spending history : \nDATE, CATEGORY, AMOUNT\n----------------------\n"
		if len(user_history)==0:
			spend_total_str = "Sorry! No spending records found!"
		else:
			for rec in user_history:
				spend_total_str += str(rec) + "\n"
			bot.send_message(chat_id, spend_total_str)
	except Exception as e:
		bot.reply_to(message, "Oops!" + str(e))	
				

#function to edit date, category or cost of a transaction
@bot.message_handler(commands=['edit'])
def edit1(m):
    read_json()
    global user_list
    chat_id = m.chat.id
    
    if (str(chat_id) in user_list):
        info = bot.reply_to(m, "Please enter the date and category of the transaction you made (Eg: 01-Mar-2021,Transport)")
        bot.register_next_step_handler(info, edit2)
    
    else:
       bot.reply_to(chat_id, "No data found")			

i_edit = -1
def edit2(m):
    global i_edit
    i_edit = -1
    chat_id = m.chat.id
    data_edit = getUserHistory(chat_id)
    info = m.text
    date_format = "^(([0][1-9])|([1-2][0-9])|([3][0-1]))\-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\-\d{4}$"
    info = info.split(',')
    x = re.search(date_format,info[0])
    if(x == None):
        bot.reply_to(m, "The date is incorrect")
        return
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    choices = ['Date','Category','Cost']
    for c in choices:
        markup.add(c)
    
    for record in data_edit:
        i_edit = i_edit + 1
        record = record.split(',')
        if info[0] == record[0][0:11] and info[1] == record[1]:
            choice = bot.reply_to(m, "What do you want to update?", reply_markup = markup)
            bot.register_next_step_handler(choice, edit3)
            break

def edit3(m):
    choice1 = m.text
    chat_id = m.chat.id
    data_edit = getUserHistory(chat_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for cat in spend_categories:
        markup.add(cat)
    if(choice1 == 'Date'):
        new_date = bot.reply_to(m, "Please enter the new date (in dd-mmm-yyy format)")
        bot.register_next_step_handler(new_date, edit_date)
        
            
    if(choice1 == 'Category'):
        new_cat = bot.reply_to(m, "Please select the new category", reply_markup = markup)
        bot.register_next_step_handler(new_cat, edit_cat)
        
                
    if(choice1 == 'Cost'):
        new_cost = bot.reply_to(m, "Please type the new cost")
        bot.register_next_step_handler(new_cost, edit_cost)        

def edit_date(m):
    global i_edit
    new_date = m.text
    date_format = "^(([0][1-9])|([1-2][0-9])|([3][0-1]))\-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\-\d{4}$"
    chat_id = m.chat.id
    data_edit = getUserHistory(chat_id)
    x1 = re.search(date_format,new_date)
    if(x1 == None):
        bot.reply_to(m, "The date is incorrect")
        return
    record = data_edit[i_edit].split(',')
    record[0] = new_date + record[0][11:len(record[0])]
    data_edit[i_edit] = record[0] + ',' + record[1] + ',' + record[2]
    user_list[str(chat_id)] = data_edit
    write_json(user_list)
    bot.reply_to(m, "Date is updated")
    
def edit_cat(m):
    global i_edit
    chat_id = m.chat.id
    data_edit = getUserHistory(chat_id)
    new_cat = m.text
    record = data_edit[i_edit].split(',')
    record[1] = new_cat
    data_edit[i_edit] = record[0] + ',' + record[1] + ',' + record[2]
    user_list[str(chat_id)] = data_edit
    write_json(user_list)
    bot.reply_to(m, "Category is updated")

def edit_cost(m):
    global i_edit
    new_cost = m.text
    chat_id = m.chat.id
    data_edit = getUserHistory(chat_id)
    
    if(validate_entered_amount(new_cost) != 0):
        record = data_edit[i_edit].split(',')                
        record[2] = new_cost
        data_edit[i_edit] = record[0] + ',' + record[1] + ',' + str(float(record[2]))
        user_list[str(chat_id)] = data_edit
        write_json(user_list)
        bot.reply_to(m, "Cost is updated")
    
    else:
        bot.reply_to(m, "The cost is invalid")
        return

#function to display total expenditure
@bot.message_handler(commands=['display'])
def command_display(message):
    read_json()
    chat_id = message.chat.id
    history = getUserHistory
    if history == None:
        bot.send_message(chat_id, "Oops! Looks like you do not have any spending records!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in spend_display_option:
            markup.add(mode)
        # markup.add('Day', 'Month')
        msg = bot.reply_to(message, 'Please select a category to see the total expense', reply_markup=markup)
        bot.register_next_step_handler(msg, display_total)

def display_total(message):
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if not DayWeekMonth in spend_display_option:
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(DayWeekMonth))

        history = getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        bot.send_chat_action(chat_id, 'typing')  # show the bot "typing" (max. 5 secs)
        time.sleep(0.5)

        total_text = ""

        if DayWeekMonth == 'Day':
            query = datetime.now().today().strftime(dateFormat)
            queryResult = [value for index, value in enumerate(history) if str(query) in value] #query all that contains today's date
        elif DayWeekMonth == 'Month':
            query = datetime.now().today().strftime(monthFormat)
            queryResult = [value for index, value in enumerate(history) if str(query) in value] #query all that contains today's date
        total_text = calculate_spendings(queryResult)

        spending_text = ""
        if len(total_text) == 0:
            spending_text = "You have no spendings for {}!".format(DayWeekMonth)
        else:
            spending_text = "Here are your total spendings {}:\nCATEGORIES,AMOUNT \n----------------------\n{}".format(DayWeekMonth.lower(), total_text)

        bot.send_message(chat_id, spending_text)
    except Exception as e:
        bot.reply_to(message, str(e))

def calculate_spendings(queryResult):
    total_dict = {}

    for row in queryResult:
        s = row.split(',')    #date,cat,money
        cat = s[1]  #cat
        if cat in total_dict:
            total_dict[cat] = round(total_dict[cat] + float(s[2]),2)    #round up to 2 decimal
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " $" + str(value) + "\n"
    return total_text

def getUserHistory(chat_id):
    global user_list
    if (str(chat_id) in user_list):
        return user_list[str(chat_id)]
    return None


#function to delete a record
def deleteHistory(chat_id):
    global user_list
    if (str(chat_id) in user_list):
        del user_list[str(chat_id)]
    return user_list

#handles "/delete" command
@bot.message_handler(commands=['delete'])
def command_delete(message):
    global user_list
    chat_id = message.chat.id
    read_json()
    delete_history_text = ""
    if (str(chat_id) in user_list):
        write_json(deleteHistory(chat_id))
        delete_history_text = "History has been deleted!"
    else:
        delete_history_text = "No records there to be deleted. Start adding your expenses to keep track of your spendings!"
    bot.send_message(chat_id, delete_history_text)

def addUserHistory(chat_id, user_record):
	global user_list
	if(not(str(chat_id) in user_list)):
		user_list[str(chat_id)]=[]
	user_list[str(chat_id)].append(user_record)
	return user_list

def main():
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(3)
        print("Connection Timeout")

if __name__ == '__main__':
    main()
