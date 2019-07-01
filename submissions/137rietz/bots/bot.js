// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

const { ActivityHandler, builder } = require('botbuilder');
const { UserProfile } = require('../userProfile');
const posTagger = require('wink-pos-tagger');

const USER_PROFILE = 'USER_PROFILE';

class LadderBot extends ActivityHandler {
    /**
     *
     * @param {ConversationState} conversationState
     * @param {UserState} userState
     * @param {Dialog} dialog
     * @param {any} logger object for logging events, defaults to console if none is provided
     */
    constructor(conversationState, userState, dialog, logger) {
        super();
        if (!conversationState) throw new Error('[DialogBot]: Missing parameter. conversationState is required');
        if (!dialog) throw new Error('[DialogBot]: Missing parameter. dialog is required');
        if (!logger) {
            logger = console;
            logger.log('[DialogBot]: logger not passed in, defaulting to console');
        }

        //state management objects
        this.conversationState = conversationState;
        this.userState = userState;
        this.storage = conversationState.storage;

        this.dialog = dialog;
        this.logger = logger;

        //posTagger instantiation
        this.tagger = posTagger();

        //state property assessors
        this.dialogState = this.conversationState.createProperty('DialogState');
        this.userProfile = this.userState.createProperty(USER_PROFILE);

        this.onMessage(async (context, next) => {
            this.logger.log('Bot//React to onMessage');
            const userProfile = await this.userProfile.get(context, new UserProfile());
            //send activity to bot: newUserInput --> Client recognizes validated input and updates vizualization  
            await context.sendActivity({ type: 'event', name: 'newUserInput', value: [context._activity.text, userProfile.currentSeed, await this.getNouns(context._activity.text)] });
            // Run the Dialog with the new message Activity.
            await this.dialog.run(context, this.dialogState, this.userProfile);

            /*console.log('/// state property accessor: ' + JSON.stringify(userProfile));
            console.log('//--> user profile is :: iteration ' + userProfile.iteration + ' // current seed: ' + userProfile.currentSeed);*/

            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });

        this.onDialog(async (context, next) => {
            this.logger.log('Bot//React to onDialog');
            // Save any state changes. The load happened during the execution of the Dialog.
            await this.conversationState.saveChanges(context, false);
            await this.userState.saveChanges(context, false);

            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });
    }

    async getNouns(text) {
        let token = await this.tagger.tagSentence(text);
        let result = [];
        await token.forEach(word => {
            if(word.pos == 'NN') {
                result.push(word.value);
            }
        });
        return await result;
    }
}

module.exports.LadderBot = LadderBot;


        
