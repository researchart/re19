// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
const appInsights = require('applicationinsights');
appInsights.setup('be188060-fb68-4558-8568-f71e575ebba8').start();

//import relevant database modules (sqlite3)
const sqlite3 = require('sqlite3').verbose();

const dotenv = require('dotenv');
const path = require('path');
const restify = require('restify');

// Import required bot services.
// See https://aka.ms/bot-services to learn more about the different parts of a bot.
const { BotFrameworkAdapter, MemoryStorage, ConversationState, UserState, TranscriptLoggerMiddleware, ConsoleTranscriptLogger } = require('botbuilder');
// This bot's main dialog.
const { MainDialog } = require('./dialogs/mainDialog');
const { WelcomeBot } = require('./bots/welcomeBot');
// This is the pregenerated list of attributes for laddering
const { CustomLogger } = require('./mat/CustomLogger');

// Import required bot configuration.
const ENV_FILE = path.join(__dirname, '.env');
dotenv.config({ path: ENV_FILE });

// Create HTTP server
const server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, () => {
    console.log(`\n${ server.name } listening to ${ server.url }`);
    console.log(`\nLadderBot up and running // ready to elicit`);
    console.log(`\nWaiting for user input :)`);
});

// Create adapter.
// See https://aka.ms/about-bot-adapter to learn more about how bots work.
const adapter = new BotFrameworkAdapter({
    appId: process.env.MicrosoftAppId,
    appPassword: process.env.MicrosoftAppPassword
});

//Create LoggerMiddleware
const customLogger = new CustomLogger();
const loggerMiddleware = new TranscriptLoggerMiddleware(customLogger);
//register middleware with BotFrameworkAdapter
adapter.use(loggerMiddleware);

// Define state store for your bot.
// See https://aka.ms/about-bot-state to learn more about bot state.
const memoryStorage = new MemoryStorage();

// Create user and conversation state with in-memory storage provider.
const conversationState = new ConversationState(memoryStorage);
const userState = new UserState(memoryStorage);

// Pass in a logger to the bot. For this sample, the logger is the console, but alternatives such as Application Insights and Event Hub exist for storing the logs of the bot.
const logger = console;

// Create the main dialog.
const dialog = new MainDialog(userState);
const bot = new WelcomeBot(conversationState, userState, dialog, logger);

// Catch-all for errors.
adapter.onTurnError = async (context, error) => {
    // This check writes out errors to console log .vs. app insights.
    console.error(`\n [onTurnError]: ${ error }`);
    // Send a message to the user
    await context.sendActivity(`Oops. Something went wrong!`);
    // Clear out state
    await conversationState.load(context);
    await conversationState.clear(context);
    // Save state changes.
    await conversationState.saveChanges(context);
};

// Listen for incoming requests.
server.post('/api/messages', (req, res) => {
    adapter.processActivity(req, res, async (context) => {
        // Route to main dialog.
        await bot.run(context);
    });
});
