document.addEventListener("DOMContentLoaded", ()=>{
});

function load_page(page){

}


function getUser(){
    fetch("currentuser")
    .then(response => response.json)
}
// will do somehing with it later when ill be able to write APIS SPA

function Edit(){

    const button = document.querySelector("#edit");

    button.addEventListener('click', function(event){
        let  parent = event.target.parentElement;
        console.log(parent.id);
    });

}