import json
import openai
from collections import defaultdict
import gpts
from itertools import product
from itertools import combinations
import random

import os

# products_file = 'products.json'
item_corpus_file = os.path.join(os.path.dirname(__file__), '../data/gpt_autoGene/itemCorpus.json')
concept_refs_file = os.path.join(os.path.dirname(__file__), '../data/gpt_autoGene/conceptRefs.json')
delimiter = "####"


def create_category_message():
    system_message_content = f"""
            You are a teacher of the course "Medienpädagogik und Medienkommunikation" .\
            The most recent user query will be delimited with \
            {delimiter} characters.
            Output a python list of objects, where each object has \
            the following format:
                'category': <list of topics or subject>,
                'definition': <text to define the theme>

            Only output the list of objects, with nothing else.
            """

    user_message_content = f""" 
           Please list of the content what I should study. \
            """

    combined_messages = gpts.prompts.customize_prompt(system_message_content, user_message_content, "")
    print("sys+user messages: ", combined_messages)
    return combined_messages


def create_ref_message(concepts):
    # concept = "Media Literacy"
    # concept1 = "Digital Citizenship"
    system_message_content = f"""
               You are a expert on the topic of "Medienpädagogik und Medienkommunikation" .\
               The most recent user query will be delimited with \
               {delimiter} characters.
               
               Output a python list of objects (max 3 most influential of references or literatures of  \
               research papers or articles) from journal or conferences or books, where each object has \
               the following format:
                   'Title': <title of the research paper or article>,
                   'Authors': <list of the authors>,
                   'Source': <Journal or Conference or Book>,
                   'Date': <month, year. Both if possible>,
                   'Summary': <summary of the paper or article>   

               Only output the list of objects, with nothing else.
               """

    user_message_content = f""" 
              Can you please provide me some literatures which covers all of {delimiter}{concepts}{delimiter} 
               """

    combined_messages = gpts.prompts.customize_prompt(system_message_content, user_message_content, "")
    print("sys+user messages: ", combined_messages)
    return combined_messages


def get_gpt_response(messages, filename):
    response = gpts.test_gpt.get_completion0(messages, model="gpt-3.5-turbo")
    print("topics of MM: ", response['text'])

    ctext = response['text'].replace('\n', '').replace('"', '').replace('\'', '"')
    json_object = json.loads(ctext)
    # print("type(json_object) is: ", type(json_object)) # type(json_object) is:  <class 'list'>

    with open(filename, "w") as write_file:
        json.dump(json_object, write_file, indent=4)
    return None


def auto_generate_itemCorpus():
    combined_mass = create_category_message()
    get_gpt_response(combined_mass, item_corpus_file)
    return None


## below for retrieving references

# get references of one concept
def get_concept_ref(concepts_string):
    combined_mass = create_ref_message(concepts_string)
    #get_gpt_response(combined_mass, concept_refs_file)
    response = gpts.test_gpt.get_completion0(combined_mass, model="gpt-3.5-turbo")
    # print("topics of MM: ", response['text'])

    ctext = response['text'].replace('\n', '').replace('"', '').replace('\'', '"')
    json_object = json.loads(ctext)
    return json_object


def auto_generate_references():
    # # 1. read and load concepts from .json
    # num_combination = 4
    # filename = os.path.join(os.path.dirname(__file__), '../data/gpt_autoGene/itemCorpus1.json')
    # with open(filename, 'r') as f:
    #     response = f.read()
    #     response = response.replace('\n', '')
    #     response = response.replace('}{', '},{')
    #     if not response.startswith("["):
    #         response = "[" + response
    #     if not response.endswith("]"):
    #         response = response + "]"
    #     data = json.loads(response)
    # # print('data is', data)
    # print('type(data): ', type(data)) # list
    # concept_list = []
    # for obj in data:
    #     concept_list.extend(obj['category'])
    # print('concept_list :', concept_list)
    #
    # # 2. get combination of concept list, max 4 concepts as one search string
    # concepts_list= get_combined(concept_list, num_combination)
    #
    # # 3. for each concept to get a list of its
    all_refers =[]
    # # since gpt-3.5 does not allow to be used for retrieving a big amount of data,
    # # sampled_list = random.sample(concepts_list, 10)


    concepts_list= ['Media Education', 'Media Communication Theories', 'Mass Communication', 'Interpersonal Communication',
     'Media Literacy', 'Digital Citizenship', 'Media and Society', 'Media Production', 'Media Ethics', 'Media Law',
     'Media Regulation']
    #for concepts in sampled_list:
    for concepts in concepts_list:
        #resultStrs = ','.join(map(str, concepts))
        resultStrs = concepts
        #print('resultString is: ', resultStrs)
        refer_list= get_concept_ref(resultStrs)
        temp_dic= {"concepts":resultStrs,  "references": refer_list}
        print("temp_dic is: ", temp_dic)
        all_refers.append(temp_dic)

    print("all refers are: ",all_refers)
    with open(concept_refs_file, "w") as write_file:
        json.dump(all_refers, write_file, indent=4)
    return None


def combine(temp_list, m):
    temp_list2 = []
    for c in combinations(temp_list, m):
        temp_list2.append(c)
    return temp_list2


# only limited 4 combined concepts as a search string
def get_combined(user_list, n):
    end_list = []
    # for i in range(len(user_list)):
    for i in range(n+1):
        end_list.extend(combine(user_list, i))
    print("end_list :", end_list)
    return end_list


# def get_concpt_ref():
#     concept= "Media Literacy"
#     concept1= "Digital Citizenship"
#
#     system_message_content = f"""
#            You are a expert on the topic of "Medienpädagogik und Medienkommunikation" .\
#            The most recent user query will be delimited with \
#            {delimiter} characters.
#            Output a python list of objects, where each object has \
#            the following format:
#                'Title': <title of the research paper or article>,
#                'Authors': <list of the authors>,
#                'Source': <Journal, Conference, or Books>,
#                'Date': <month, year. Both if possible>,
#                'Summary': <summary of the paper or article>
#
#            Only output the list of objects, with nothing else.
#            """
#
#     user_message_content = f"""
#           Can you please provide me max 3 references or literatures of the most \
#           influential research papers or articles from journal or conferences or books on the topic of {delimiter}{concept}{delimiter}
#            """
#
#     combined_messages = gpts.prompts.customize_prompt(system_message_content, user_message_content, "")
#     print("sys+user messages: ", combined_messages)
#     response = gpts.test_gpt.get_completion0(combined_messages, model="gpt-3.5-turbo")
#
#     print("topics of MM: ", response['text'])
#
#     ctext = response['text'].replace('\n', '').replace('"', '').replace('\'', '"')
#     json_object = json.loads(ctext)
#     # print("type(json_object) is: ", type(json_object)) # type(json_object) is:  <class 'list'>
#
#     with open(concept_refs_file, "w") as write_file:
#         json.dump(json_object, write_file, indent=4)
#
#     return None


# def auto_generate_itemCorpus(messages):
    # system_message_content = f"""
    #     You are a teacher of the course "Medienpädagogik und Medienkommunikation" .\
    #     The most recent user query will be delimited with \
    #     {delimiter} characters.
    #     Output a python list of objects, where each object has \
    #     the following format:
    #         'category': <list of topics or subject>,
    #         'definition': <text to define the theme>
    #
    #     Only output the list of objects, with nothing else.
    #     """
    #
    # user_message_content = f"""
    #    Please list of the content what I should study. \
    #     """
    #
    # combined_messages = gpts.prompts.customize_prompt(system_message_content, user_message_content, "")
    # print("sys+user messages: ", messages)


    # response = gpts.test_gpt.get_completion0(messages, model="gpt-3.5-turbo")
    #
    # # print("topics of MM: ", response['text'])
    #
    # ctext = response['text'].replace('\n', '').replace('"', '').replace('\'', '"')
    # json_object = json.loads(ctext)
    # # print("type(json_object) is: ", type(json_object)) # type(json_object) is:  <class 'list'>
    #
    # with open(item_corpus_file, "w") as write_file:
    #     json.dump(json_object, write_file, indent=4)
    #
    # return response

