// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

//require the used prompts and dialog flows
const { 
    ChoicePrompt,
    ComponentDialog, 
    DialogSet, 
    DialogTurnStatus, 
    WaterfallDialog 
} = require('botbuilder-dialogs');

//require the used dialog subfiles
const { UserProfile } = require('../userProfile');
const Attributes = require('../mat/attributes.json');

//Here we would add additional dialoges, such as top level dialoge etc. see example. Currently, we do not have additional dialoges

const SEED_DIALOG = 'SEED_DIALOG';
const CHOICE_PROMPT = 'CHOICE_PROMPT';
const WATERFALL_DIALOG = 'WATERFALL_DIALOG';

class SeedDialog extends ComponentDialog {
    constructor() {
        super(SEED_DIALOG);
        console.log('---- Initiate SeedDialog ----');

        //Instantiation of various dialog forms used in mainDialog.js
        this.addDialog(new ChoicePrompt(CHOICE_PROMPT));

        this.addDialog(new WaterfallDialog(WATERFALL_DIALOG, [
            this.initialStep.bind(this),
            this.reportBackStep.bind(this),
        ]));

        this.initialDialogId = WATERFALL_DIALOG;
    }
    //Prompt user to select seed
    async initialStep(stepContext) {
        //create instance of user profile to save seed

        stepContext.values.seedStepData = new UserProfile(0,'new','new', Attributes.list);
        //first iteration
        if(stepContext.options == 'initiate') {
            stepContext.values.seedStepData.iteration = 1;
        } 
        //subsequent iterations
        else {
            stepContext.values.seedStepData.iteration = stepContext.options[0] + 1;
            stepContext.values.seedStepData.seedList = stepContext.options[1];
        }
        //attributes are loaded from json and subsequently adapted and saved in stepContext memory / user Profile
        return await stepContext.prompt(CHOICE_PROMPT, {
            prompt: 'Please select the service from the list that you think would be the most promising for students.',
            retryPrompt: 'Please make sure you select an option from the list',
            choices: stepContext.values.seedStepData.seedList
        });
    }

    //Prompt selected seed and await first 'consequence' reply, no special questionning technique here
    async reportBackStep(stepContext) {
        stepContext.values.seedStepData.currentSeed = stepContext.result.value;

        //remove the selected seed from the seedList for that user
        for( var i = 0; i < stepContext.values.seedStepData.seedList.length; i++) { 
            if ( stepContext.values.seedStepData.seedList[i] == stepContext.result.value) {
                stepContext.values.seedStepData.seedList.splice(i, 1); 
            }
        }

        const userProfile = stepContext.values.seedStepData;

        return await stepContext.endDialog(userProfile);
    }
}

module.exports.SeedDialog = SeedDialog;
module.exports.SEED_DIALOG = SEED_DIALOG;