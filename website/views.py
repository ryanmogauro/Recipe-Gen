from flask import Blueprint, render_template, redirect, url_for
from flask import request
import os
from openai import OpenAI

# Create a blueprint
main_blueprint = Blueprint('main', __name__)
OPENAI_KEY = os.environ.get('OPEN_AI_KEY')


def generateRecipe(ingridients):

    content_text = f"I am starving and still need to make dinner. Please give me a recipe for something to make! I have a full kitchen and these ingridients: {ingridients}"

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


@main_blueprint.route('/', methods=['GET', 'POST'])
# @login_required
def main_page():
    return render_template('index.html')
    

@main_blueprint.route('/get-recipe', methods=['GET', 'POST'])
def get_recipe():

    if request.method == 'POST':

        # we got the request as a json object
        data = request.get_json()       
        ingridients = data['input']
        print("ING: ", ingridients)

        recipe = generateRecipe(ingridients)
        
        print("recipe: ", recipe)

        return {"recipe": recipe}