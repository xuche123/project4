document.addEventListener('DOMContentLoaded', function () {
    const follow = document.querySelector('#follow')
    if (follow) {
        follow.addEventListener('click', () => {
            user = follow.dataset.id
            fetch(`/follow/`, {
                method: 'POST',
                body: JSON.stringify({
                    follow: user
                })
            })
                .then(response => response.json())
                .then(result => {
                    console.log(result)
                    if (result['type'] == 'follow') {
                        follow.innerHTML = 'Following'
                    }
                    else {
                        follow.innerHTML = 'Follow'
                    }
                    document.querySelector('#follower-count').innerHTML = result['follower_count']
                });
        });
    }
});
