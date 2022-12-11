const hostname = document.getElementById('hostname');
const nextBtn = document.getElementById('next');
const connection = document.getElementById('connection');
const targetIP = document.getElementById('targetIP');

async function gethostname() {
    return await eel.gethostname()();
}

gethostname()
    .then(name => {
        console.log(name)
        hostname.value = name;
    })

nextBtn.addEventListener('click', () => {
    console.log('nextBtn click')
    eel.signSupporter(hostname.value);
    nextBtn.disabled = true;
    hostname.disabled = true;
})

eel.expose(supporterConnected);
function supporterConnected(address) {
    targetIP.innerText = `${address} 連線中`;
    connection.style.display = 'flex';
    setTimeout(() => {
        connection.style.opacity = '1';
    }, 100)
}

eel.expose(supporterDisonnected);
function supporterDisonnected() {
    connection.style.opacity = '0';
    setTimeout(() => {
        connection.style.display = 'none';
    }, 400)
}

function disconnect() {
    eel.supporterDisconnect()()
        .then(supporterDisonnected);
}