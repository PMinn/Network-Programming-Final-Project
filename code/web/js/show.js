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

var lastMoveTime = new Date();
img.addEventListener('mousemove', e => {
    var now = new Date();
    if (now - lastMoveTime > 200) {
        eel.mousemove(Math.floor(e.offsetX * supportWidth / img.width), Math.floor(e.offsetY * supportHeight / img.height));
        lastMoveTime = now;
    }
})

document.body.addEventListener('contextmenu', e => {
    e.preventDefault();
    e.stopPropagation();
    return false;
}, false);
document.body.addEventListener('mousedown', e => mouse_event(0, e), false);
document.body.addEventListener('mouseup', e => mouse_event(1, e), false);
function mouse_event(type, e) {
    var clickPositionX = Math.floor(e.offsetX * supportWidth / img.width);
    var clickPositionY = Math.floor(e.offsetY * supportHeight / img.height);
    if (e.isTrusted) {
        if (type == 0) {
            if (e.button == 0) eel.mousedownLeft(clickPositionX, clickPositionY);
            else if (e.button == 2) eel.mousedownRight(clickPositionX, clickPositionY);
        } else {
            if (e.button == 0) eel.mouseupLeft(clickPositionX, clickPositionY);
            else if (e.button == 2) eel.mouseupRight(clickPositionX, clickPositionY);
        }
    }
    e.preventDefault();
    e.stopPropagation();
    return false;
}

img.addEventListener('wheel', e => {
    eel.wheel(e.deltaX, e.deltaY);
    e.stopPropagation();
    return false;
});

var keyTable = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    'command', 'option', 'optionleft', 'optionright'];
function convertKey(e) {
    var keyLowerCase = e.key.toLowerCase();
    var key = '';
    if (keyTable.includes(keyLowerCase)) key = keyLowerCase;
    else if (keyLowerCase == 'control') key = 'ctrl'
    return key;
}

img.addEventListener("keydown", e => {
    var key = convertKey(e);
    eel.keydown(key);
    e.preventDefault();
    e.stopPropagation();
}, false);

img.addEventListener("keyup", e => {
    var key = convertKey(e);
    eel.keyup(key);
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