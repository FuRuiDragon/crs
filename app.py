import gpts.test_gpt as gpts
import gpts.prompts as pm
# import example.products_request.products as pr
import knowledge.ItemCorpus as ic
from flask import jsonify, redirect
import termpaper.utils as tpu
import termpaper.tp as tp
from flask import Flask, g, render_template, request

start_time = gpts.start_time
modelList = ["gpt-3.5-turbo (OpenAI)", "gpt-4 (OpenAI)", "LLaMA2 (Meta)", "Gemini (Goggle)","Claude2 (Anthropic)", ]

current_model = gpts.model


app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html", modelList=modelList, gpt_model=current_model, starting_time=start_time)


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        current_model = request.form.get('current_model')
        print('now you have switched to model: ',  current_model)
    return '', 204


@app.route("/get")
def get_bot_response():
    user_input_text = request.args.get('msg')
    user_message = user_input_text

    # if request.method == 'POST':
    #     current_model = request.form.get('current_model')
    #     print('current xxx model: ',  current_model)

    if user_input_text.startswith("0: "):
        return tp.ask_gpt_directly(user_input_text.replace("0: ",""))
    else:
        # to get Term paper recommendations
        print('xxx the changed current model: ', current_model)
        response, all_msgs = tp.process_stu_message(user_message, [])
        print("\n final response: ", response)
        print("\n  all messages: ", all_msgs)
        return response


if __name__ == "__main__":
    gpts.get_apikey()
    app.run(host="0.0.0.0", debug=True)
