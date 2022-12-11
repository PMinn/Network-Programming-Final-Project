const page = document.getElementById('page');

function connect2support(uid) {
    eel.changePage("show")()
        .then(() => {
            location = `./show.html?uid=${uid}`;
        })
}

function renderList() {
    page.innerHTML = '';
    eel.getSupporter()()
        .then(supporters => {
            supporters = JSON.parse(supporters);
            supporters.forEach(supporter => {
                var computer = document.createElement('div');
                computer.classList.add('computer');
                var lastCheckTime = new Date(parseFloat(supporter.lastCheckTime) * 1000);
                computer.innerHTML = `
                            <div class="icon">
                                <img src="./media/monitor.png" alt="">
                            </div>
                            <div class="info">
                                <div class="name">${supporter.hostname}</div>
                                <div>線上</div>
                            </div>
                        `;
                if (supporter.isRuning == "True") {
                    computer.classList.add('hidden');
                } else {
                    computer.onclick = () => {
                        connect2support(supporter.uid);
                    }
                }
                page.appendChild(computer);
            });
            console.log(supporters)
        })
}

renderList();
setInterval(renderList, 2000);