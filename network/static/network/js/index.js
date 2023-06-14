document.addEventListener("DOMContentLoaded", ()=>{
    Like();
    Edit();
    ProfileChecker();
})

function ProfileChecker(){
    if(document.querySelector("#username").innerHTML === document.querySelector("profile_username")){
        document.querySelector("#follow").className = "btn btn-danger disabled";
    }

}

function Edit(){
    const buttons = document.querySelectorAll("#edit");
    buttons.forEach(button =>{
        button.addEventListener('click', function(event){

            let post = event.target.parentElement.closest('div');
            text = post.children[1].innerHTML;
            document.querySelector(".edit-post-form").innerHTML = `
            <label for="exampleFormControlTextarea1">Edit your post:</label>
            <textarea class="form-control" id="edit-post" rows="3">${text}</textarea>     
            `;
            const submitButton = document.querySelector("#save");
            submitButton.addEventListener('click', ()=>{
            document.querySelector("#close").click();
            editedText = document.querySelector("textarea").value;
            post.children[1].innerHTML = editedText;
            fetch(`edit/${post.id}`, {
                method: 'POST',
                body: JSON.stringify({
                    editedText : editedText
                })
              })
        });
    });
})
}

// will do somehing with it later when ill be able to write APIS SPA

//Like function
function Like(){

const likeButtons = document.querySelectorAll("#like");

likeButtons.forEach(button =>{
    
    button.addEventListener('click', function(event){
        let post = event.target.parentElement.closest('div');
        fetch(`like/${post.id}`, {
            method: "PUT",
            body: JSON.stringify({
                //liked:
            })
        })
        .then(response => response.json())
        .then(function(result){ 
            result = JSON.stringify(result)
            liked = JSON.parse(result).like

            if(liked === true){
                btn = event.target
                btn.innerHTML = "Unlike"
            }
            if(liked === false){
                btn = event.target
                btn.innerHTML = "Like"
            }
        })
    })
})

}