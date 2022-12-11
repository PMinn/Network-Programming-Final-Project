const img = document.getElementById('img');
var supportWidth = 1920;
var supportHeight = 1080;
var supportRatio = supportWidth / supportHeight;
var lastDblickPositionX = 0, lastDblickPositionY = 0;
var keyborEvent = {
    shift: false,
    ctr: false,
    alt: false
}
function checkImgSize() {
    if (window.innerWidth / window.innerHeight > supportRatio) {
        img.style.height = '100%';
        img.style.width = 'auto';
    } else {
        img.style.height = 'auto';
        img.style.width = '100%';
    }
}

window.addEventListener('resize', checkImgSize, true);
checkImgSize();

img.addEventListener('mousemove', e => {
    console.log(e.offsetX * supportWidth / img.width, e.offsetY * supportHeight / img.height)
    eel.mousemove(e.offsetX * supportWidth / img.width, e.offsetY * supportHeight / img.height)
})

img.addEventListener('click', e => {
    var clickPositionX = Math.floor(e.offsetX * supportWidth / img.width);
    var clickPositionY = Math.floor(e.offsetY * supportHeight / img.height);
    // setTimeout(() => {
    //     if (clickPositionX != lastDblickPositionX || clickPositionY != lastDblickPositionY)
    console.log('click', clickPositionX, clickPositionY);
    // }, 300)
});

// img.addEventListener('dblclick', e => {
//     lastDblickPositionX = Math.floor(e.offsetX * supportWidth / img.width);
//     lastDblickPositionY = Math.floor(e.offsetY * supportHeight / img.height)
//     console.log('dblclick', lastDblickPositionX, lastDblickPositionY);
// });
document.addEventListener("keydown", e => {
    console.log('keydown', event)
    keyborEvent.shift = e.shiftKey;
    keyborEvent.ctr = e.ctrlKey;
    keyborEvent.alt = e.altKey;
    e.preventDefault();
    e.stopPropagation();
}, false);
document.addEventListener("keypress", e => {
    e.preventDefault();
    e.stopPropagation();
}, false);
document.addEventListener("keyup", e => {
    console.log('keyup', e)
    keyborEvent.shift = e.shiftKey;
    keyborEvent.ctr = e.ctrlKey;
    keyborEvent.alt = e.altKey;
    e.preventDefault();
    e.stopPropagation();
}, false);

var uuid = location.search.replace('?uid=', '');
if (uuid != '') {
    eel.connect2Supporter(uuid);
}

eel.expose(readImg);
function readImg(base64) {
    img.src = base64;
}

eel.expose(targetDisconnect);
function targetDisconnect() {
    var dialog = new Dialog({
        text: '連線已斷開',
        btns: [{
            text: '確定',
            onclick: () => {
                eel.changePage('access')()
                    .then(() => {
                        location = './access.html';
                    })
            }
        }]
    });
    dialog.show();
}

eel.expose(setImgSize);
function setImgSize(width, height) {
    supportWidth = width;
    supportHeight = height;
    supportRatio = supportWidth / supportHeight;
    checkImgSize();
}

function disconnect() {
    eel.accessDisconnect()()
        .then(() => {
            location = './access.html';
        })
}