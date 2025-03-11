"""Defines needed endpoints"""
import os
from flask import Blueprint, render_template
from flask import request
from openai import OpenAI

main_blueprint = Blueprint('main', __name__)
OPENAI_KEY = os.environ.get('OPEN_AI_KEY')

@main_blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    """Renders main page"""
    return render_template('index.html')

@main_blueprint.route('/get-recipe', methods=['GET', 'POST'])
def get_recipe():
    """Get recipe endpoint, which calls generateRecipe()"""
    if request.method == 'POST':

        # we got the request as a json object
        data = request.get_json()
        ingridients = data['input']
        print("ING: ", ingridients)

        recipe = generate_recipe(ingridients)

        print("recipe: ", recipe)

        return {"recipe": recipe}

def generate_recipe(ingridients):
    """Calls OpenAI API using ingridients param"""

    content_text = """I am starving and still need to make dinner. 
    lease give me a recipe for something to make! 
    I have a full kitchen and these ingridients:
    """
    content_text+=str(ingridients)
    
    client = OpenAI(api_key=OPENAI_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        #store=True,
        messages=[
            {"role": "user", "content": content_text}
        ]
    )
    if completion.choices[0].message.content == None:
        return "Sorry, I don't understand that."

    return completion.choices[0].message.content
