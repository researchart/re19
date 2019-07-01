// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
const sqlite3 = require('sqlite3').verbose();

const {
	TextPrompt,
	WaterfallDialog,
	ComponentDialog, 
    DialogSet, 
    DialogTurnStatus
} = require('botbuilder-dialogs');

const LADDERING_DIALOG = 'LADDERING_DIALOG';

const TEXT_PROMPT = 'TEXT_PROMPT';
const WATERFALL_DIALOG = 'WATERFALL_DIALOG';

class LadderingDialog extends ComponentDialog {
	constructor() {
		super(LADDERING_DIALOG);
		console.log('---- Initiate LadderingDialog ----');

		//this.ladderingReply = null;

		this.addDialog(new TextPrompt(TEXT_PROMPT));
		this.addDialog(new WaterfallDialog(WATERFALL_DIALOG, [
			this.questionStep.bind(this),
			this.loopStep.bind(this)
		]));

		this.initialDialogId = WATERFALL_DIALOG;
	}

	//This is to be repeated dynamically until user exit event occures. Questions are choosen on random.
	async questionStep(stepContext) {
			//extract options from current stepContext
			const ladderingReply = stepContext.options;
			//ladderingReply[0] = initial reply, ladderingReply[1] = answer, [2] = current seed
			stepContext.values.initialReply = ladderingReply[0];
			stepContext.values.ladderingSeedSave = ladderingReply[2];
			stepContext.values.lastTechnique = ladderingReply[3];
			//insert repeatable dialog options here
			let message = '';

			//-- Selection 'intelligence' for laddering technique selection
			const max = 6; //number of possible dialog options for the bot to choose from (4 interviewing techniques + x 'standard' dialog options)
			let rnd = Math.floor(Math.random() * Math.floor(max));
			while(rnd === stepContext.values.lastTechnique) {
				rnd = Math.floor(Math.random() * Math.floor(max));
			}
			//-- End laddering question selectionn

			//follow up question to previous layer or initiate new layer
			if(stepContext.values.lastTechnique === 0) {
						message = "What would the service need to have to mitigate these problems?";
			} 
			//what question - to elicit attributes of a system
			else if(stepContext.values.lastTechnique === 9) {
						message = "What about the service makes you think it would do that?";
						stepContext.values.lastTechnique = 9;
			}
			else if(stepContext.values.lastTechnique === 8) {
						message = "Initially you gave the following reason why you think that *" + stepContext.values.ladderingSeedSave + "* is important: *" + ladderingReply[0] + "*. What about the service makes you think it would do that?";
						stepContext.values.lastTechnique = 9;
			} 
			//if no follow up is required
			else {
				switch (rnd) {
					//negative laddering
					case 0:
						message = "What problems could be caused by this?";
						break;
					//exclusion
					case 1:
						message = 'What alternatives for this are there for students today? What are shortcomings of these services?';
						break;
					//retrospective
					case 2:
						message = 'Has your perception of this changed compared to a couple of years ago? If so, why is that and what changed?';
						break;
					//clarification - tbd when saving of input in files works.
					case 3:
						message = "Okay, you just said *" + ladderingReply[1] + "*, right? In the context of *" + ladderingReply[2] + "*, could you explain that to me in more detail?";
						break;
					//standard why question
					default:
						message = 'Why is that important?';
				}	
			}
			
			//initiate prompt options
			let promptOptions = { prompt: message }; //if message should be displayed as well, add >> + '*' + ladderingReply + '*'
			//save current question for next iteration as long as interview isn't in attribute section (lastTechnique = 9)
			if(stepContext.values.lastTechnique != 9) {
				stepContext.values.lastTechnique = rnd;
			}
			//after randomly selecting a dialog option, prompt user input here
			return await stepContext.prompt(TEXT_PROMPT, promptOptions);
	}

	async loopStep(stepContext) {
		//check for stop command
		if(stepContext.result == 'stop' || stepContext.result == 'Stop' || stepContext.result == 'STOP' || stepContext.result.startsWith("stop") || stepContext.result.startsWith("Stop")) {
			if(stepContext.values.lastTechnique != 9) {
				//ask for concrete attribute in a system
				return await stepContext.replaceDialog(LADDERING_DIALOG, [stepContext.values.initialReply, stepContext.result, stepContext.values.ladderingSeedSave, 8]);
			}
			else {
				return await stepContext.endDialog();
			}
		}
		//options: [user replay, seed for current line of conversation, last laddering technique applied]
		return await stepContext.replaceDialog(LADDERING_DIALOG, [stepContext.values.initialReply, stepContext.result, stepContext.values.ladderingSeedSave, stepContext.values.lastTechnique]);
	}
}

module.exports.LadderingDialog = LadderingDialog;
module.exports.LADDERING_DIALOG = LADDERING_DIALOG;