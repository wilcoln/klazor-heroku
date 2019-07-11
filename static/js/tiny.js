document.onclick = closeAllContextMenu // Close all context menu on click

function closeAllContextMenu(){
    let contextmenus = document.querySelectorAll('.rmenu');
    for(let contextmenu of contextmenus)
        contextmenu.className = "rmenu hide"
}
function openFolderContextMenu(e, id) {
    e.preventDefault()
    closeAllContextMenu()
    let contextmenuId = "fmenu_" + id
    document.getElementById(contextmenuId).className = "rmenu show";
    document.getElementById(contextmenuId).style.position = 'absolute';
    document.getElementById(contextmenuId).style.top = e.clientY*.001 + 'px';
    document.getElementById(contextmenuId).style.left = e.clientX*.25 + 'px';

    window.event.returnValue = false;
}

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