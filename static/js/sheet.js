// Navbr and toolbar animation
 let threshold = $('.sheet-breadcrumb').length ? 60:10;
onscroll = function () {
    let sheetToolbar = $(".sheet-toolbar");
    if (scrollY > threshold) {
        sheetToolbar.css('background', 'whitesmoke')
        sheetToolbar.css('box-shadow', '0 0 .5rem rgba(0,0,0,.1)')
    } else {
        sheetToolbar.css('background', 'transparent')
        sheetToolbar.css('box-shadow', 'none')
    }
}