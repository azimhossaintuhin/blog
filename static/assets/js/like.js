const like = document.getElementById('color_heart')
const like_count = document.getElementById('color_heart_count')

like.onclick = () => {
    const blogid = like.getAttribute('data-blog');
    const url  = `/like/${parseInt(blogid)}`
    fetch(url ,{
        method : 'GET',
        headers : {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
       
        return response.json();

    }).then(data => {
        if(data.liked){
            like.classList.add('heart_color');
        }else{
            like.classList.remove('heart_color');
        }
        like_count.innerHTML = data.like_count;
        
    })
    .catch(err => {
        console.log(err);
    })
}