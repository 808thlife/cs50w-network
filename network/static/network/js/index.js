const buttons = document.querySelectorAll("#edit");
    buttons.forEach(button =>{

        button.addEventListener('click', function(event){
            let post = event.target.parentElement.closest('div');
            console.log(post.closest("p"));
            document.querySelector("textarea").value = post.closest("p");
            fetch(`edit/${post.id}`, {
                method: 'POST',
                body: JSON.stringify({
                    editedText : document.querySelector("textarea").value
                })
              })
              .then(response => response.json())
              .then(result => {
                  // Print result
                  console.log(result);
              })
        });

    })
    



function load_page(page){

}


function getUser(){
    fetch("currentuser")
    .then(response => response.json)
}
// will do somehing with it later when ill be able to write APIS SPA

