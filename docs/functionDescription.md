start_and_menu_command(m)
- Function that defines how the /start and /help commands have to be handled/processed

command_add(message)
- Function that defines how the /add command has to be handled/processed

post_category_selection(message)
- Function that processes that validates the entered category, and accepts amount as input accordingly

post_amount_input(message)
- Function that writes the entered amount into the user's json file once the amount is validated 

validate_entered_amount(amount_entered)
- Function that validates the entered amount for non-string values

AddUserHistory(chat_id, user_record)
- Function to update expenditure details in the json file as and when user adds them

deleteHistory(chat_id)
- Function to delete previous expenditure history of the user

getUserHistory(chat_id):
- Function to fetch user history and display it in the bot window

show_history(message)
- Function to display expendtiture history
- Error message displayed when no history present

command_display(message)
- Function to display total expenditure in a day or month, depending on the user input

display_total(message)
- Function to retrieve spending data per category from user history and return total expense

calculate_spendings(queryResult)
- Function to calculate the total expense per category from the queryResult

edit1(m)
- Function to take input from user about date and the category of the transaction they want to update
- Once user gives the correct details, function edit2 is triggered

edit2(m)
- Based on user's input from edit1, this function checks the field the user wants to update (Date, Category or Cost)
- The choice selected by the user is passed to edit3

edit3(m)
- Based on the information received from edit2, one of the following function is triggered: edit_cat, edit_date or edit_cost

edit_cat(m)
- This function is triggered if user inputs Category in edit2 function
- It will ask user for new category and update the record accordingly

edit_date(m)
- This function is triggered if user inputs Date in edit2 function
- It will ask user for new date and update the record accordingly

edit_cost(m)
- This function is triggered if user inputs Cost in edit2 function
- It will ask user for new cost and update the record accordingly

command_select(m)
- Function that defines how the /Search has to be handled/processed

product_table(m)
- This function is triggered if the user enters a product name for comparing the prices

find_user_by_username(username)
- This function searches the user from the input username

get_sharing_details(m)
- This function is called if the user wants to split up the bill with other users

post_sharing_selection(m)
- Function that takes input of other user ids for splitting up the bill

handle_user_id_input_for_sharing(m)
- This function stores the info of other users among whom the bills should be splitted

send_update_to_user_about_expense(m,u)
- tThe function which sends other users about their splits

add_bill_to_database(m)
- Function stores the split details in database , also check if limits are set and notify if they are crossed

validate_entered_amount(a)
- Functions checks the entered amount is valid or nt (numerical)

command_delete(m)
- Function delete data from database regarding all the splits

command_limit(m)
- Function takes input whether the limit should be set for day/Month/Year

post_limit_category_selection(m)
- The Function sets takes the input data and sets the limit in selected category

post_limit_amount_input(message)
- The function saves the limit details to database and also validates the entered amount

command_settle(m)
- Function takes the input transaction to be settled

settle_up(m)
- The function retrieves the transaction to be settled and displays the users share to settle

choice_for_settle(m,user_record)
- The function takes the final confirmation if the user wants to settle the record

post_settle_selection(m, user_record)
- The fucntion settles the expense selected and updates the database.


