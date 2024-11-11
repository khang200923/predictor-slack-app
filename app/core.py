from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv("..")
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
base_message = ""
with open("message.md", "r", encoding="utf-8") as f:
    base_message = f.read()

def message(data: str, today: datetime = datetime.now()):
    return base_message.format(data=data, today=today.strftime("%Y/%m/%d"))

class Prediction(BaseModel):
    no: list[str]
    yes: list[str]
    thinking: str
    tentative: float
    reflecting: str
    answer: float

def predict(data: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": message(data)}
        ],
        response_format=Prediction
    )

    return completion

def format_prediction(prediction) -> str:
    no_list = "\n".join([f"* {item}" for item in prediction["no"]])
    yes_list = "\n".join([f"* {item}" for item in prediction["yes"]])

    formatted_string = (
        f"*Reasons for 'no'*: \n{no_list}\n\n"
        f"*Reasons for 'yes'*: \n{yes_list}\n\n"
        f"*Thinking*: {prediction["thinking"]}\n"
        f"*Tentative probability*: {prediction["tentative"]*100:.1f}%\n"
        f"*Reflecting*: {prediction["reflecting"]}\n"
        f"*Final probability*: {prediction["answer"]*100:.1f}%\n"
    )
    return formatted_string
