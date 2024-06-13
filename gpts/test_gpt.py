import openai
import os
import pandas as pd
from json2html import *
from datetime import datetime

openai.api_key = os.environ['OPENAI_API_KEY']
tempStr = openai.api_key
model = "gpt-3.5-turbo"
model35 = "gpt-3.5-turbo"
model4 = "gpt-4"
openai.api_key =''


myobj = datetime.now()
start_time = str(myobj.hour) + ':' + str(myobj.minute)


# print('start_time: ', start_time)


def get_apikey():
    # print(tempStr)
    print('model name: ', model)


def get_completion_price(total_tk):
    # Set Header Names
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../data/openai_gpt35_turbo_price.csv')

    columns = ['Tokens per execution', 'Price for 1 execution']
    df = pd.read_csv(filename, header=1, names=columns)
    # Iterate all rows using DataFrame.iterrows()
    for index, row in df.iterrows():
        if total_tk <= row["Tokens per execution"]:
            price = row["Price for 1 execution"]
            break
    # print(price)
    print(type(price))
    return price


# moderation, evaluate inputs
def get_moderation(user_message):
    response = openai.Moderation.create(
        input=user_message
    )
    # moderation_output = response.results[0]
    # print(moderation_output)
    flagged = response.results[0]["flagged"]
    return flagged


# this is a simple, straight forward question/response to/from chatGPT model
def get_completion0(messages,
                    model=model4,#"gpt-3.5-turbo",
                    temperature=0,
                    max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
        max_tokens=max_tokens,  # the maximum number of tokens the model can ouptut
    )
    completion_price = get_completion_price(response.usage["total_tokens"])
    data = dict({'text': response.choices[0].message["content"],
                 'prompt_tokens': response.usage["prompt_tokens"],
                 'completion_tokens': response.usage["completion_tokens"],
                 'total_tokens': response.usage["total_tokens"],
                 'completion_price': completion_price,
                 'chain_of_thoughts': ""})
    return data


delimiter = "####"


def get_completion_from_messages(messages,
                                 model=model4, #"gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    global chain_of_thoughts
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
        max_tokens=max_tokens,  # the maximum number of tokens the model can ouptut
    )
    # return response.choices[0].message["content"]

    # content_json = json.dumps(response.choices[0].message["content"], sort_keys=True, indent=4, separators=(',', ': '))
    # print(content_json)
    temp_text = response.choices[0].message["content"]
    # print('temptext: ', temp_text)
    if not temp_text or temp_text != "[]":
        separator = "Response to user"
        chain_of_thoughts = temp_text.split(separator, 1)[0].rstrip().replace('####', "")
        # print('cot: ', chain_of_thoughts)
        try:
            final_response = temp_text.split(delimiter)[-1].strip()
            print('final response: \n ', final_response)
            if final_response == chain_of_thoughts or chain_of_thoughts == "[]":
                chain_of_thoughts = ""
        except Exception as e:
            final_response = "Sorry, I'm having trouble right now, please try asking another question."

        content_json = json2html.convert(json=final_response.replace("'", ""))
        # print(content_json)
    else:
        content_json = "Sorry, I can not find any answer now. Please try asking another question."
        chain_of_thoughts = ""

    completion_price = get_completion_price(response.usage["total_tokens"])
    data = dict({'text': content_json,
                 'prompt_tokens': response.usage["prompt_tokens"],
                 'completion_tokens': response.usage["completion_tokens"],
                 'total_tokens': response.usage["total_tokens"],
                 'completion_price': completion_price,
                 'chain_of_thoughts': chain_of_thoughts})
    return data
