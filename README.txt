SETUP INSTRUCTIONS:
    1. Install latest version of python. Installation guide for windows --> ( https://techdator.net/install-python-windows-10/ )
    2. Open a command prompt in the bot folder ( The folder where all the files of the bot are. ) or
    change directory to the bot folder from command prompt.
    3. Run command "pip install -r requirements.txt" to install the required modules for the bot.
    4. Now rename the file called "sample-config.py" to "config.py".
    5. Now follow this guide --> ( https://core.telegram.org/api/obtaining_api_id ) to register an app 
    on telegram portal and get your api_id and api_hash and put it in the config.py.
    6. Follow this guide --> ( https://docs.activechat.ai/docs/messaging-channels/telegram/creating-bots-with-botfather/ ) to
    create a bot on botfather and get your bot token and paste in config.py
    7. Put your telegram phone number in config.py.
    8. Put the names of all the 5 channels in config.py in the order same as the sample signals
    file you sent me.
    9. Now run the get_id.py file using "python get_id.py" command and it will ask you for username,
    Enter your username and it will show you telegram ID, Copy that id and put in config.py file as ADMIN_TG_ID.
    10. Now go to metaapi.cloud and copy your API key and put in config.py file.
    11. Next you can change your broker timezone if you want and your lot size.
    12. Now save config.py file and exit.
    13. Run the bot using "python main.py" command. The bot will ask you for confirmation code sent to your telegram app.
    And in the teleram app the bot will ask you to link your mt4 account with bot. 
    14. After linking the account just shutdown the bot and restart.
    15. Now you should be getting signals from source channels and executing on the mt4.
    16. Let me know if you find any problems.