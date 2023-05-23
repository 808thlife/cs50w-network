document.addEventListener("DOMContentLoaded", ()=>{


const button = document.querySelector("#follow");

button.addEventListener('click', function(){
    const name = document.querySelector("#profile_username");
    fetch(`profile/${name}`, {
        method: "PUT",
        body: JSON.stringify(

        )
    })
    .then(response => response.json());
});

});

function load_page(page){

}

// will do somehing with it later when ill be able to write APIS SPA

