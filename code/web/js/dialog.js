function Dialog({ text = '請放入訊息', btns = [] }) {
    this.dialog_out = document.createElement('div');
    this.dialog_out.classList.add('dialog-out');
    this.dialog = document.createElement('div');
    this.dialog.classList.add('dialog');
    this.h3 = document.createElement('h3');
    this.h3.innerText = text;
    this.btnGroup = document.createElement('div');
    this.btnGroup.classList.add('btn-group');
    this.dialog_out.appendChild(this.dialog);
    this.dialog.appendChild(this.h3);
    this.dialog.appendChild(this.btnGroup);
    btns.forEach(btn => {
        var btn_dom = document.createElement('div');
        btn_dom.classList.add('btn');
        btn_dom.innerText = btn.text;
        btn_dom.onclick = btn.onclick;
        this.btnGroup.appendChild(btn_dom);
    });
    document.body.appendChild(this.dialog_out);
    this.show = function () {
        this.dialog_out.classList.add('show');
    }
    this.hidden = function () {
        this.dialog_out.classList.remove('show');
    }
}