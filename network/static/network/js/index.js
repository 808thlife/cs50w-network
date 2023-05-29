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
            editedText = document.querySelector("textarea").value;
            post.children[1].innerHTML = "edited";
            console.log(editedText);
            fetch(`edit/${post.id}`, {
                method: 'POST',
                body: JSON.stringify({
                    editedText : editedText
                })
              })
        });
    });
})
// will do somehing with it later when ill be able to write APIS SPA

