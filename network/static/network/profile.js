document.addEventListener('DOMContentLoaded', function () {
    const follow = document.querySelector('#follow')
    if (follow) {
        follow.addEventListener('click', () => {
            user = follow.dataset.id
            // console.log(user)
            fetch(`/follow/`, {
                method: 'POST',
                body: JSON.stringify({
                    follow: user
                })
            })
                .then(response => response.json())
                .then(result => {
                    // console.log(result)
                    console.log(result['type'])
                    if (result['type'] == 'follow') {
                        follow.innerHTML = 'Unfollow'
                    }
                    else {
                        follow.innerHTML = 'Follow'
                    }
                });
        });
    }
});
