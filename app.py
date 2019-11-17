"""
This program performs the following action:

1. uses /question command to send a user a create question button
2. create a dialog box to capture user question
3. Sends to public channel

Pending
1. Creating a Text file for loading static enviroment variables and tokens
2. Retrieve user ID from /question endpoint i.e. "/slack/command", methods=["POST"]
3. Refactor code.
"""


import json
import os

from flask import Flask, Response, jsonify, make_response, request
from slack import WebClient

slack_client = WebClient(
    token="xoxb-829744125652-839421312695-ftDiwN2TEyjlvEJk4RiD4GJC")

app = Flask(__name__)

QUESTIONS_DICT = {}

# This is required for testing once command slash is implemented.
Qst_channel = "CQGCA22G6"
user_id = "UQG1VUM2T"


@app.route("/slack/command", methods=["POST"])
def openFloor():
    """API endpoint for "/question" command.

    Outstanding: We should retrieve user_id and channel from the API endpoint payload
    """
    question_dm = slack_client.chat_postMessage(
        channel=user_id,  # pick user ID from slack command response
        text="I am Questionbot ::robot_face::, and I\'m here to help send your question :grey_question:",
        attachments=[{
            "text": "",
            "callback_id": user_id + "question_form",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [{
                "name": "question_box",
                "text": ":grey_question: Ask Question",
                "type": "button",
                "value": "question_box"
            }]
        }]
    )

    # Create a new question for this user in the QUESTIONS_DICT dictionary
    QUESTIONS_DICT[user_id] = {
        "question_channel": question_dm["channel"],
        "message_ts": "",
        "question": {}
    }
    return make_response("", 200)


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    """ API endpoint for interactive message

    Outstanding: 
    """
    def post_message(channel_, userid_, message_):
        """Simple function to post message to channel or direct message

        Outstanding: Modify code for Direct message"""
        slack_client.chat_postMessage(
            channel=channel_,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message_
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "reply",
                                "emoji": True
                            },
                            "value": "click_me_123"
                        }
                    ]
                }
            ]
        )

    # Parse the request payload
    message_action = json.loads(request.form["payload"])
    user_id = message_action["user"]["id"]

    if message_action["type"] == "interactive_message":
        # Add the message_ts to the user's question info
        QUESTIONS_DICT[user_id]["message_ts"] = message_action["message_ts"]

        # Show the question dialog to the user
        open_dialog = slack_client.dialog_open(
            trigger_id=message_action["trigger_id"],
            dialog={
                "callback_id": user_id + "qst_form",
                "title": "BigBlue Question Bot",
                "submit_label": "Submit",
                "elements": [
                    {
                        "label": "What's your Question",
                        "name": "question",
                        "type": "textarea",
                        "placeholder": "maximum of 300 character",
                        "hint": "Provide additional information if needed.",
                    },
                    {
                        "label": "Session",
                        "name": "session",
                        "type": "text",
                        "placeholder": "enter related session",
                        "optional": True
                    }
                ]
            }
        )

        print(open_dialog)

        # Update the message to show that qstbot is taking user's question
        slack_client.chat_update(
            # QUESTIONS_DICT[user_id]["question_channel"],
            channel=message_action["channel"]["id"],
            ts=message_action["message_ts"],
            text=":pencil: Taking your question...",
            attachments=[]
        )

    elif message_action["type"] == "dialog_submission":
        question_box = QUESTIONS_DICT[user_id]

        # Update the message to show that we're in the process of taking their question
        slack_client.chat_update(
            channel=QUESTIONS_DICT[user_id]["question_channel"],
            ts=question_box["message_ts"],
            text=":white_check_mark: Question received!",
            attachments=[]
        )

        # retrieving payload message_action
        user_name = message_action["user"]["name"]
        session = message_action["submission"]["session"] if message_action["submission"]["session"] else "None"
        message_block = "from: " + user_name + ":wave: \n\nquestion: " + \
            message_action["submission"]["question"] + \
            ":question:\n\nsession: " + session

        # Post to administrator
        admin_id = "DQDMWKX6G"  # Update admin_id to actual admin ID.
        post_message(Qst_channel, admin_id, message_block)

    return make_response("", 200)


@app.route("/slack/message_actions", methods=["POST"])
def delete_method():
    slack_client.chat_delete(channel, ts)(
        """ API endpoint to delete a chat"""
    )
    return make_response("", 200)


if __name__ == "__main__":
    app.run(debug=True)
