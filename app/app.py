import sys
import core
import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from dotenv import load_dotenv

load_dotenv()

#TODO: Implement security

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.command("/predictgpt")
def predictgpt(ack, say, command):
    ack("_Predicting..._")
    res = core.predict(command["text"])
    data = json.loads(res.choices[0].message.content)
    say(f"""Prediction for \"{command["text"]}\" (given by <@{command["user_id"]}>):

{core.format_prediction(data)}""")
    print("Submitted prediction with command:")
    print(command)

if __name__ == "__main__":
    # app.start(port=int(os.environ.get("PORT", 3000)))
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
