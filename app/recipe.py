import requests

def get_recipe_details(id):
     url = f"https://api.edamam.com/api/recipes/v2/{id}"
    
     headers = {
         'x-rapidapi-key': "5f8d15e8",
         'x-rapidapi-host': "7e4f94d1f57158c014144b6f0864dc56"
     }
     response = requests.get(url, headers=headers)
     print(response.json())
     return response.json()