document.addEventListener('DOMContentLoaded', function () {
    const edit = document.querySelectorAll('.edit')
    edit.forEach(function (edit) {
        edit.addEventListener('click', () => {
            post = edit.dataset.id
            content = document.querySelector(`#content-${post}`)
            content.innerHTML = `<textarea id="edit-${post}" class="form-control" rows="4">${content.textContent}</textarea>`
            const save = document.createElement('button')
            save.className = 'btn'
            save.id = `save-${post}`
            save.innerHTML = '<i class="bi bi-check-lg"></i>'

            edit.replaceWith(save)
            document.querySelector(`#save-${post}`).addEventListener('click', () => {
                new_content = document.querySelector(`#edit-${post}`).value
                new_content = new_content.trim()
                fetch(`/edit/`, {
                    method: 'POST',
                    body: JSON.stringify({
                        post_id: post,
                        content: new_content
                    })
                })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result)
                        content.innerHTML = new_content
                        save.replaceWith(edit)
                    });
            });
        });
    });
});