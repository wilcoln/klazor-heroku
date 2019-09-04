function openTinyFolderContextMenu(e, id) {
    let contextmenuId = "fmenu_" + id
    openContextMenu(e, contextmenuId)
}

function openTinySheetContextMenu(e, id) {
    let contextmenuId = "smenu_" + id
    openContextMenu(e, contextmenuId)
}
function openTinyCourseContextMenu(e, id) {
    let contextmenuId = "cmenu_" + id
    openContextMenu(e, contextmenuId)
}

function openTinyFileContextMenu(e, id) {
    let contextmenuId = "file-menu_" + id
    openContextMenu(e, contextmenuId)
}
function copyFileUrl(fileLocation){
    let url = getAppLocation() + fileLocation
    copyTextToClipboard(url)
}
function getAppLocation(){
    return location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
}
function copySheetUrl(id){
    // Change this in production mode
    let url = getAppLocation() + '/sheet/' + id
    copyTextToClipboard(url)
}
function copyTextToClipboard(textValue){
    /* Select the text field */
    let inputElt = document.createElement("input")
    inputElt.type = 'text'
    inputElt.value = textValue
    document.body.append(inputElt)
    inputElt.select()
    /* Copy the text inside the text field */
    document.execCommand("copy");
    document.body.removeChild(inputElt)
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