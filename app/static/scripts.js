let searchButton = document.querySelector('#search')


//Add an event listner to the buttonthat runs the function sendApiRequest when it is clicked
searchButton.addEventListener("click", ()=>{
    console.log("button clicked")
    sendApiRequest()
})

//An ansychronous function to fetch data from the API

async function sendApiRequest(){
    let APP_ID = '5f8d15e8'
    let API_KEY = '7e4f94d1f57158c014144b6f0864dc56'

    let response = await fetch(`https://api.edamam.com/search?app_id=${APP_ID}&app_key=${API_KEY}&q=lamb`);
    console.log(response)
    let data = await response.json()
    console.log(data)
    useApiData(data)

}

// function that does something with API 

function useApiData(data){
    document.querySelector("#content").innerHTML = `
    <div class="card col-3 offset-1"   style="width: 18rem;">
  <img src="${data.hits[0].recipe.image}" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">${data.hits[0].recipe.label}</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    <a href="${data.hits[0].recipe.url}" class="btn btn-primary">Recipe</a>
  </div>
</div>
     `    
}