let searchButton = document.querySelector('#search')

// Function to fetch and display data
function fetchAndDisplayData(inputValue) {
    let APP_ID = '5f8d15e8';
    let API_KEY = '7e4f94d1f57158c014144b6f0864dc56';
    let resultsCount = 52; // the number of recipes displayed on page load

   // calling the api
    var apiUrl = `https://api.edamam.com/search?app_id=${APP_ID}&app_key=${API_KEY}&q=${inputValue}&to=${resultsCount}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => useApiData(data))
        .catch(error => console.error('Error:', error));
}

// Function to handle search button click
searchButton.addEventListener('click', function() {
 var inputValue = document.getElementById('searchInput').value;
 fetchAndDisplayData(inputValue);
});

// Call fetchAndDisplayData when the page loads
window.onload = function() {
 var foodItems = ['apple', 'banana', 'bread', 'carrot', 'chicken', 'fish', 'grape', 'kiwi', 'lemon', 'mango', 'orange', 'pineapple', 'strawberry', 'tomato', 'watermelon']; // Replace this with your list of food items
 var randomIndex = Math.floor(Math.random() * foodItems.length);
 var randomFoodItem = foodItems[randomIndex];
 fetchAndDisplayData(randomFoodItem); // Fetch and display data for a random food item when the page loads
};

function useApiData(data) {
    if (data.hits && data.hits.length > 0) {
        let content = '<div class="card-container">';
        data.hits.forEach(hit => {
            let recipeUri = hit.recipe.uri;
            let recipeId = recipeUri.split('#recipe_')[1];
            let recipeUrl = `/recipe/${recipeId}`;

            let ingredients = hit.recipe.ingredientLines;
            let ingredientList = ingredients.map(ingredient => `<li>${ingredient}</li>`).join('');
            content += `
                <div class="card col-6 offset-2 card-custom" style="width: 22rem;">
                    <h5><a href="${recipeUrl}" onclick="getRecipe('${recipeId}')">${hit.recipe.label}</a></h5>
                    <a href="${recipeUrl}" onclick="getRecipe('${recipeId}')">
                        <img src="${hit.recipe.image}" class="card-img-top" alt="..." onclick="getRecipe('${recipeId}')">
                    </a>
                    <div class="card-body">
                    </div>
                </div>
                `;

        });
        content += '</div>';
        document.querySelector("#content").innerHTML = content;
    } else {
        console.error('No hits found in the API response');
    }
}

 
 function getRecipe(recipeId) {
    fetch(`/recipe/${recipeId}`)
        .then(response => response.json())
        .then(data => {
            // Handle the returned data here
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
 }
 