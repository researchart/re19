# LadderBot

A bot that uses the laddering interviewing technique to conduct requirements elicitation interviews with end-users.

The bot is enhanced by a JavaScript based visualization, which can be accessed by loading the file ladderbot.html in a browser. Therefore, a few prerequisites have to be met, as outlined in section "To run the bot in a browser". A detailed description of the bot can be found in section "Further information on LadderBot".

This bot has been created using [Bot Framework](https://dev.botframework.com).

## Prerequisites

- [Node.js](https://nodejs.org) version 10.14.1 or higher

    ```bash
    # determine node version
    node --version
    ```
### Depencencies
- applicationinsights: version 1.3.1 or higher
- botbuilder: version 4.4.0 or higher
- botbuilder-dialogs: version 4.4.0 or higher
- dotenv version: 7.0.0 or higher
- restify version: 8.2.0 or higher
- sqlite3 version: 4.0.8 or higher
- wink-pos-tagger: version 2.2.2 or higher

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

### Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- File -> Open Bot
- Enter a Bot URL of `http://localhost:3978/api/messages`

### To run the bot in a browser

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

## Instructions on using the bot

Currently, LadderBot is capable of conducting a three step laddering interview on the topic "smartphone services for students". Instructions are provided by the bot during its use. In a nutshell, the following procedure will be followed by LadderBot.
1. Ask the user to select one out of five services as seed for the laddering interview
2. Engage in a series of questions
3. Wait for the user to end the series of questions with the command 'stop'
4. Switch to a second stage of the current step, asking "what?" questions to identify concrete system attributes
5. Continue the questioning until the user ends the series with the command 'stop'
6. Repeat steps 1 - 5 for a total of three times
7. End the laddering interview

* The visualization in the browser version will update for every attribute, consequence, value taken from user input. For stop commands, as well as selection (that are primarily numeric), the visualization will be paused.
* Data collected by the bot will be saved using sqlite3, the location of the database-file may be changed in the CustomLogger.js file

## Further information on LadderBot
LadderBot is an end-user requirements self-elicitation system using the laddering interview technique. The system is currently in a pre-final state, with most of its functionalities working. It is capable of conducting a laddering interview with end-users and visualizing the interview structure in a graphical interface.
LadderBot is configurated to elicit consequences and values for three attributes. The list of attributes for the evaluation will be generated in a pre-test session, via triadic sorting. LadderBot asks the user to identify the most relevant attribute from the list. This attribute is used as seed for the ACV chain until the users switch to the next attribute, for which the selection process is repeated, excluding already chosen attributes. When asking why-questions repeatedly, the chatbot will rely on four techniques for rephrasing questions to help and guide the user. Peer-reviewed guidelines for human interviewers on how to conduct laddering interviews inspired the utilized techniques. For now, the four techniques are applied by LadderBot at random. However, no technique may be used two times in a row. The visualization of the current status of the interview on the left side updates itself for each elicited consequence before LadderBot asks the next question. To end the elicitation for a specific attribute, or the interview in general, a human interviewer would need to identify when an interviewee has reached the ‘end’ of an ACV chain. As the current iteration of LadderBot is not capable of recognizing whether a user has already described all values for a chain of consequences, the bot requires the user to indicate if they want to continue the laddering process for the current attribute, or switch to the next chain. The user can make this indication using the command ‘stop’. After eliciting three ACV chains, LadderBot ends the interview.

## Deploy the bot to Azure

To learn more about deploying a bot to Azure, see [Deploy your bot to Azure](https://aka.ms/azuredeployment) for a complete list of deployment instructions.

## Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Dialogs](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
- [Gathering Input Using Prompts](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-prompts?view=azure-bot-service-4.0)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
- [Azure Portal](https://portal.azure.com)
- [Language Understanding using LUIS](https://docs.microsoft.com/en-us/azure/cognitive-services/luis/)
- [Channels and Bot Connector Service](https://docs.microsoft.com/en-us/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)
- [Restify](https://www.npmjs.com/package/restify)
- [dotenv](https://www.npmjs.com/package/dotenv)