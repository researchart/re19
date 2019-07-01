// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

//require the used prompts and dialog flows
const { 
    ChoicePrompt,
    TextPrompt, 
    ComponentDialog, 
    DialogSet, 
    DialogTurnStatus, 
    WaterfallDialog 
} = require('botbuilder-dialogs');

//require the used dialog subfiles
const { SeedDialog, SEED_DIALOG } = require('./seedDialog');
const { LadderingDialog, LADDERING_DIALOG } = require('./ladderingDialog');
const { UserProfile } = require('../userProfile');
//Here we would add additional dialoges, such as top level dialoge etc. see example. Currently, we do not have additional dialoges

const MAIN_DIALOG = 'MAIN_DIALOG';
const WATERFALL_DIALOG = 'WATERFALL_DIALOG';
const TEXT_PROMPT = 'TEXT_PROMPT';

//Initiate control variables / settings for laddering dialog
const maxRepetitions = 3;

class MainDialog extends ComponentDialog {
    constructor(userState) {
        super(MAIN_DIALOG);
        console.log('---- Initiate MainDialog ----');

        //Instantiation of various dialog forms used in mainDialog.js
        this.addDialog(new SeedDialog());
        this.addDialog(new LadderingDialog());
        this.addDialog(new TextPrompt(TEXT_PROMPT));
        
        this.addDialog(new WaterfallDialog(WATERFALL_DIALOG, [
            this.seedStep.bind(this),
            this.engageInterviewStep.bind(this),
            this.ladderingStep.bind(this),
            this.finalStep.bind(this)
        ]));

        this.initialDialogId = WATERFALL_DIALOG;
    }

    /**
     * The run method handles the incoming activity (in the form of a TurnContext) and passes it through the dialog system.
     * If no dialog is active, it will start the default dialog.
     * @param {*} turnContext
     * @param {*} accessor
     */
    async run(turnContext, accessor, userAccessor) {
        const dialogSet = new DialogSet(accessor);
        dialogSet.add(this);

        this.userProfile = userAccessor;

        const dialogContext = await dialogSet.createContext(turnContext);
        const results = await dialogContext.continueDialog();
        if (results.status === DialogTurnStatus.empty) {
            await dialogContext.beginDialog(this.id);
        }
    }

    //Start seed and laddering step
    async seedStep(stepContext) {
        //process stepContext.options for iteration input
        if(JSON.stringify(stepContext.options) == "{}") {
            //First iteration
            return await stepContext.beginDialog(SEED_DIALOG, 'initiate');
        }
        else {
            //every subsequent iteration
            return await stepContext.beginDialog(SEED_DIALOG, stepContext.options);
        }
    }

    //send first message to react to selected seed
    async engageInterviewStep(stepContext) {
        //retrieve information from previous seedStep
        stepContext.values.userData = new UserProfile();
        stepContext.values.userData = stepContext.result;

        //save change of iteration+currentSeed to stable userProfile
        await this.userProfile.set(stepContext.context, stepContext.values.userData);

        console.log('- - - - - - - - -');
        console.log('> Engaging reaction to seed Step ');

        //check if seed has changed, if true, notifiy client about the changes
        const userProfile = await this.userProfile.get(stepContext.context, new UserProfile());
            //check if seed has changed, if true, notifiy client about the changes
            if(userProfile.currentSeed != userProfile.seedComparision) {
                //notify client that seed has changed --> build new branch in visualization
                await stepContext.context.sendActivity({ type: 'event', name: 'seedChange', value: userProfile.currentSeed });
                userProfile.seedComparision = userProfile.currentSeed;
                await this.userProfile.set(stepContext.context, userProfile);
            }
            
        //initiate appropriate response
        await stepContext.context.sendActivity('Please answer the following questions to the best of your knowledge and ability.');
        return await stepContext.prompt(TEXT_PROMPT, {
            prompt: 'You selected *' + stepContext.values.userData.currentSeed + '* as a promising service for students. Why would this be important?',
            retryPrompt: 'Text Retry Prompt'
        });
    }

    //engage in continuous laddering interview steps
    async ladderingStep(stepContext) {
        console.log('- - - - - - - - -');
        console.log('> Engaging continuous laddering interview Step: ');
        //initiate repeatable laddering dialog
        return await stepContext.beginDialog(LADDERING_DIALOG, [stepContext.result, stepContext.result, stepContext.values.userData.currentSeed]);
    }

    //End dialog
    async finalStep(stepContext) {
        //reset seed, keep current iteration
        stepContext.values.userData.currentSeed = null;
        //if iterations < max interations: replace dialog with new iteration of main dialog
        if(stepContext.values.userData.iteration < maxRepetitions) {
            return await stepContext.replaceDialog(MAIN_DIALOG, [stepContext.values.userData.iteration, stepContext.values.userData.seedList]);
        }
        //if max iterations, end the dialog with the bot
        await stepContext.context.sendActivity('THANK YOU for completing this laddering interview with us, see you again soon!');
        return await stepContext.endDialog();
    }
}

module.exports.MainDialog = MainDialog;
module.exports.MAIN_DIALOG = MAIN_DIALOG;
