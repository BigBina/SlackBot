const slackBot = require('slackbots');
const axios = require('axios');

const bot = new slackBot({
    name: 'Question Bot',
    token: 'xoxb-729135212305-817655337810-vEc3OAGBIuyQ6Jhi4M0Pz8HJ'
});

var repsonseMessage = "What is your question?";

bot.on('start', () => {
    const params = {
        icon_emoji: ':question:'
    };
    bot.postMessageToChannel(
        'random',
        'Yo Whats up Just testing this out, today is November 11, 2019',
        params
    );
});

//respnes to data

function handleMessage(message) {
    if(message.includes(' ?')){
        console.log(responseMessage);
    }
}



