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
                        like.innerHTML = 'unlike'
                    }
                    else {
                        like.innerHTML = 'like'
                    }
                    count.innerHTML = result['count']
                });
        });
    });
});