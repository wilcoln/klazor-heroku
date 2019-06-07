function deleteFolder(id) {
    axios({
        method: 'post',
        url: '/folder/delete/' + id + '/',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
        }
    }).then((response) => {
        console.log(response)
    }).catch((error) => {
        console.log(error)
    });
}

function deleteSheet(id) {
    axios({
        method: 'post',
        url: '/sheet/delete/' + id + '/',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
        }
    }).then((response) => {
        console.log(response)
    }).catch((error) => {
        console.log(error)
    });
}

function showDeleteButton(e) {
    e.firstElementChild.nextElementSibling.lastElementChild.lastElementChild.style.display = 'inline-block'
}

function hideDeleteButton(e) {
    e.firstElementChild.nextElementSibling.lastElementChild.lastElementChild.style.display = 'none'
}