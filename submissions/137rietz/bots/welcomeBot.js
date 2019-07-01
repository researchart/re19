// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

const { LadderBot } = require('./bot');

class WelcomeBot extends LadderBot {
    constructor(conversationState, userState, dialog, logger) {
        super(conversationState, userState, dialog, logger);

        this.onMembersAdded(async (context, next) => {
            this.logger.log('- - - - - - - - -');
            this.logger.log('> Starting welcoming Bot' + context.activity.recipient.name);
            //send welcoming messages
            //when bot enters chat, bot sends a welcome message. When client enters chat, message was already send, so dont compute new message
            if(context.activity.membersAdded[0].name == "LadderBot") {
                await context.sendActivity('Welcome to LadderBot');
                await context.sendActivity('Please allow me to ask you a set of questions to learn more about your preferences and requirements for new services for students.');
                await context.sendActivity('For the remainder of the interview, whenever you feel like you cannot provide more information for the current line of questioning, just type "stop". You will then either be asked a different set of questions, or the interview will continue with another topic.'); 
                await context.sendActivity('Are you ready? :)');
            }
               
            //return await stepContext.beginDialog(TOP_LEVEL_DIALOG);
            this.logger.log('Finished initalStep');

            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });
    }
}

module.exports.WelcomeBot = WelcomeBot;
