import json
import openai
from collections import defaultdict

import os

topic_file = os.path.join(os.path.dirname(__file__), '../data/gpt_autoGene/itemCorpus0.json')
refer_file = os.path.join(os.path.dirname(__file__), '../data/gpt_autoGene/conceptRefs.json')

delimiter = "####"


def get_completion_from_messages(messages, model, temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    result = response.choices[0].message["content"]
    # print("\n\nMessage: ", messages)
    # print("\n\nResult: ", result)
    return result


def openfile(filename):
    with open(filename, 'r') as file:
        result_list = json.load(file)
    return result_list


# get category from file "itemCorpus0.json"
def get_topic_list():
    """
    Used in L4 to get a flat list of products
    """
    topics = openfile(topic_file)
    topic_list = []
    for topic in topics:
        # topic_list.append(topic['category'])
        topic_list.extend(topic['category'])
    return topic_list


def reference_count():
    count = 0
    concept_refers = openfile(refer_file)
    # print(concept_refers)
    for cf in concept_refers:
        count += len(cf['references'])
    print("In all, the no. of references is: ", count)
    return count


# match/search references of concepts from the file conceptRefs.json
def find_references(concepts):
    concept_refers = openfile(refer_file)
    # print(concept_refers)
    reference_list = []
    for cf in concept_refers:
        cf_list = cf['concepts'].split(",")
        intersection_list = [val for val in concepts if val in cf_list]
        count= len(intersection_list)
        # print("len(intersection_list) is: ", count )
        if count > 1:
            for item in cf['references']:
                item['star'] = count
                if item['Title'] not in [re['Title'] for re in reference_list]:
                    reference_list.append(item)
    sorted_list = sorted(reference_list, key=lambda x: x['star'], reverse=True)
    print("no. references found: ", len(reference_list))
    return sorted_list, len(reference_list)


def find_topics(user_input, category_and_topic):
    delimiter = "####"

    #print("user_input (before) :", user_input)
    system_message = f"""
    As a teacher of the course Medienpädagogik und Medienkommunikation, you will give feedback to \
    students' term paper idea and use an understanding and analytical tone in English. \
    You will be provided with a short text from a student about the ideas of a term paper.\
    The user text will be delimited with {delimiter} characters.\
    
    Step 1: summary and extract three topics or subjects from the text and give a brief explanation\
    Step 2: find out a list of related categories for each topic or subject from the allowed categories
   
    Output a python list of json objects, where each object has the following format in English:
        'topic_or_subject': <extracted from user text>,
        'subject_explanation': < short text about each subject >,
        'related_categories': <a list of categories that must be found in the allowed categories below>
       
    Where the topics must be found or extracted from the user text.
    If a topic or subject is mentioned, it must be associated with the correct category in the allowed topics list below.
    If no topic or related category are found, output an empty list.

    The allowed topics are provided in JSON format.
    Allowed categories: {category_and_topic}
    
    Ask politely if you are satisfied with the feedback or want to ask more feedback.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
    ]
    ss= get_completion_from_messages(messages, model="gpt-3.5-turbo")
    print("find_topics() === :", ss)
    print("=== find_topics() :")

    # to guarantee the result should be in json
    if ss.startswith('{'):
        ss = [ss]

    if "```json" in ss:
        start = '```json'
        end = '```'
        ss = ss[ss.find(start) + len(start):ss.rfind(end)]
        print("new ss: ", ss)

    # print("user_input (after) :", user_input)
    return ss


