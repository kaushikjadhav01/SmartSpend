# SmartSpend

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
![GitHub contributors](https://img.shields.io/badge/Contributors-5-brightgreen)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5542548.svg)](https://doi.org/10.5281/zenodo.5542548)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
![Python CI](https://github.com/kaushikjadhav01/SmartSpend/actions/workflows/build-test.yaml/badge.svg)

<hr>

## About SmartSpend

SmartSpend is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.  
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to

### <u>Additions:</u>
- Fixed several bugs related to parsing and tracking.
- Refactored old code to suit updated structure.
- Moved away from Travis to GitHub actions for rolling builds.
- <u>Feature</u> -> Upgrade backend to use Mongo DB for better storage and access.
- - Supports cloud based central storage as well as locally hosted database.
- - Allows for free extensions since the data is stored in Object model.
- <u>Feature</u> -> Add 'share' feature to share expense with other telegram users.
- - Sends a notification message to the other user indicating the added expense.
- - Added persistent storage for future tracking and settlement of balances.
- <u>Feature</u> -> Add 'limit' faeture to work as an alarm when spending exceed preset limits.
- - Users can create limits on a daily, monthly, and yearly basis.
- - When user adds an expense, all three limits are checked.

## Demo
https://user-images.githubusercontent.com/15325746/135395315-e234dc5e-d891-470a-b3f4-04aa1d11ed45.mp4

## New Functionality
https://user-images.githubusercontent.com/95981350/194871840-4b8816b7-a634-4c4f-b247-293cedb932c8.mp4


## Installation guide

The below instructions can be followed in order to set-up this bot at your end in a span of few minutes! Let's get started:

1. This installation guide assumes that you have already installed Python (Python3 would be preferred)

2. Clone this repository to your local system at a suitable directory/location of your choice

3. Start a terminal session, and navigate to the directory where the repo has been cloned

4. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```
5. Download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/

6. Once you login to your Telegram account, search for "BotFather" in Telegram. Click on "Start" --> enter the following command:
```
  /newbot
```
7. Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with "bot" (as per the instructions on your Telegram screen)

8. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy this token for future use.

9. Create a new collection in MongoDB Cloud Atlas. In the directory where this repo has been cloned, create a .env file with format like .env.sample in this repo and replace XXXX with the actual bot name, tokens and api hash and MongoDB URLs:

10. In the Telegram app, search for your newly created bot by entering the username and open the same. Once this is done, go back to the terminal session. Navigate to the directory containing the "code.py" file and run the following command:
```
  python code.py
```
11. A successful run will generate a message on your terminal that says "TeleBot: Started polling." 
12. Post this, navigate to your bot on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!






<hr>
<p>--------------------------------------------------------------------------------------------------</p>
<p>Title:'SmartSpend'</p>
<p>Version: '1.0'</p>
<p>Description: 'An easy to use Telegram Bot to track everyday expenses'</p>
<p>Authors:'Kaushik, Surya, Pradyumna, Harshita, Aditi'</p>
<p>--------------------------------------------------------------------------------------------------</p>
