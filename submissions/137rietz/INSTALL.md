#Install the bot

## To run the bot

You will have to create an Azure account in order to use the bot and generate the relevant authentication information. 

In order to set up a Web App Bot in Azure, that will be used as setup for LadderBot, please follow the instructions provided [here](https://docs.microsoft.com/de-de/azure/bot-service/bot-service-quickstart?view=azure-bot-service-4.0).

After the setup, you will have to make two changes to the files of LadderBot, in order to authenticate with your token.

1. open the .env file in the root folder of LadderBot.
* In the .env file, you will have to provide your Microsoft App ID as well as your App password
* To identify both values, you can rely on [this](https://blog.botframework.com/2018/07/03/find-your-azure-bots-appid-and-appsecret/) manual

2. open the ladderbot.html file in the root folder of LadderBot. 
* In line 478, add your DirectLine secret. 
* You can identify your secret in Azure by navigating to the Channels menu in your Web App Bot, clicking on 'edit' next to the DirectLine channel, and using one of the secret keys provided on the following page.

- Install modules

    ```bash
    npm install
    ```

- Start the bot

    ```bash
    npm start
    ```

### To run the bot in a browser including visualization

[ngrok](https://ngrok.com/) provides an instant, secure URL to localhost servers through any NAT or firewall. It is required to set up an API call of the bot against a localhost address without the need for the Bot Framework Emulator. This enables the usage of the bot via the Webchat channel.

More information on *ngrok* can be found [here](https://blog.botframework.com/2017/10/19/debug-channel-locally-using-ngrok/).

After starting the bot with 
    ```bash
    npm start
    ```
the bot will run localhost on port 3978. Initiate a ngrok tunnel to this port with
    ```bash
    ./ngrok http 3978
    ```
given that your ngrok executable is in your user's root folder.

In your Azure account, navigate to your Web App Bot. Under Bot management, go to Settings. Change the Messaging endpoint URL in the Configuration settings to the Forwarding URL that ngrok provides you with, followed by /api/messages. (E.g. https://731d7a79.ngrok.io/api/messages). Save your changes.

Finally, open ladderbot.html in a browser (tested on Chrome and Safari). 

### Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- File -> Open Bot
- Enter a Bot URL of `http://localhost:3978/api/messages`

## To see if the bot is running successfully

In the console/terminal window where the bot is running, you will see the following output.

    ---- Initiate MainDialog ----
    ---- Initiate SeedDialog ----
    ---- Initiate LadderingDialog ----

    restify listening to http://[::]:3978

    LadderBot up and running // ready to elicit

    Waiting for user input :)

This is indicating that the bot is running successfully. When interacting with the bot, you will see the following output in the console/terminal:

    > Starting welcoming BotLadderBot
    Finished initalStep
    Bot//React to onDialog
    Database// Connected to in-memory sqlite database.
    Database// Connected to in-memory sqlite database.
    Database// Connected to in-memory sqlite database.
    Database// Connected to in-memory sqlite database.
    //Bot - latestMessageID: 1
    //Bot - latestMessageID: 1
    //Bot - latestMessageID: 1
    Database// Terminate in-memory sqlite database connection.
    Database// Terminate in-memory sqlite database connection.
    Database// Terminate in-memory sqlite database connection.

Any errors occurring during the usage of the bot will be logged to the console.

If you run the bot in the browser, on the right side, the chatbot should display a few welcoming messages as soon as you load the side. In that case, the bot is running fine.