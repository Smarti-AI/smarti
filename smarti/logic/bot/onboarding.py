"""handle onboarding flow for new users"""

import smarti.logic.openai as openai
from smarti.logic import db


def get_next_message(previous_messages, new_user_message):
    """get the next message from chatgpt, based on previous messages"""
    if not previous_messages:
        prompt = get_prompt("Hebrew")
        db.save_new_bot_message(prompt)

    all_messages = db.save_new_user_message(new_user_message)

    chat_gpt_new_message = openai.get_completion_from_messages(all_messages)
    print("chat_gpt_new_message", chat_gpt_new_message)
    if ":::::" in chat_gpt_new_message:
        user_data = chat_gpt_new_message.split("::::::")[1]
        print("user_data", user_data)
        chat_gpt_new_message = "Onboarding finished!"
        # we have user data now, we can save it to the database and start a new conversation
    return chat_gpt_new_message


def get_prompt(lang="English"):
    """get the onboarding prompt in requested language"""
    return """I want to build an onboarding flow on top of chatgpt. During the onboarding you need to introduce the 
            Smarti system, which helps  children to get better in math while it's providing visibility and assistance 
            to the kid parents. After that make sure to get information for the following questions:
            1. What is your name?
            2. How old are you?
            If the age is under 15, it means it's a kid, so please ask in that grade he is studying, ask for his gender.  
            Ask for parent phone number. Make questions to fit the kids age. 
            If the age is above 15, it means it's an adult. Make sure to get relation to kid, like mom, dad, brother, 
            sister, uncle, aunt, grandpa or grandma.  Ask for the child name, age, gender and the kid phone number.
            Don't mention that the calculation is based on age of 15.
            Once you have all the information, create json object with all the information in the following format:
            If the person who is talking to you is a kid, then the fields are: 
                name, age, grade, gender, parent_phone_number
            If it's an adult, the fields are:
                name, age, relation, child_name, child_phone_number
            Before you send the json object, make sure to ask the user if the information is correct. If not, ask what 
            is wrong and make sure to get correct answers. If required, ask for the information again.
            Important: Use {0} to ask questions.
            Please enclose the json object in the following format: 
                ::::::<json object>::::::
            """.format(
        lang
    )
