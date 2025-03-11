# tests/functional/test_main.py
def test_get_recipe_mac_and_cheese(client, mock_openai):
    payload = {"input": ["macaroni", "cheese"]}
    response = client.post("/get-recipe", json=payload)
    assert response.status_code == 200

    data = response.json
    assert "recipe" in data
    assert data["recipe"] == "Here’s your mac & cheese recipe!"

def test_get_recipe_other_ingredients(client, mock_openai):
    payload = {"input": ["tomato", "chicken"]}
    response = client.post("/get-recipe", json=payload)
    assert response.status_code == 200

    data = response.json
    assert "recipe" in data
    assert data["recipe"] == "Some other generic recipe."

def test_get_recipe_no_content(client, mock_openai):
    """
    Covers the branch if completion.choices[0].message.content == None.
    We'll pass 'anything' to trigger 'content = None' in the side effect.
    """
    payload = {"input": ["anything"]}
    response = client.post("/get-recipe", json=payload)
    assert response.status_code == 200

    data = response.json
    assert "recipe" in data
    assert data["recipe"] == "Sorry, I don't understand that."

