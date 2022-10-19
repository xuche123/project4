document.addEventListener('DOMContentLoaded', function () {
    const like = document.querySelectorAll('.like')
    like.forEach(function (like) {
        like.addEventListener('click', () => {
            post = like.dataset.id
            fetch(`/like/`, {
                method: 'POST',
                body: JSON.stringify({
                    post_id: post
                })
            })
                .then(response => response.json())
                .then(result => {
                    console.log(result['type'])
                    const count = document.querySelector(`#likecount-${post}`)
                    if (result['type'] == 'like') {
                        like.innerHTML =`<i class="bi bi-heart-fill"></i>  ${result['count']}`
                    }
                    else {
                        like.innerHTML = `<i class="bi bi-heart"></i>  ${result['count']}`
                    }
                    // count.innerHTML = result['count']
                });
        });
    });
});