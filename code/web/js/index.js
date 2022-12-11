document.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
        eel.changePage(a.dataset.href)()
            .then(() => {
                location = `./${a.dataset.href}.html`;
            })
    })
})