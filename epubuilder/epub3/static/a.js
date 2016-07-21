
function hide_show(id) {
    var e = document.getElementById(id);

    if (e != null) {
        var ol = e.nextElementSibling;

        if (ol.hasAttribute('hidden') == true){
            ol.removeAttribute('hidden');
            e.innerHTML = ' ▽';

        } else {
            ol.setAttribute('hidden', 'hidden');
            e.innerHTML = ' ◀';

        }

    }

}


function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}


function set_button() {
    var master_ol = document.getElementsByTagName('ol')[0];

    var ols = master_ol.getElementsByTagName('ol');

    for (var i = 0; i < ols.length; i++) {

        var span_button = document.createElement('span');
        span_button.setAttribute('style', 'cursor:pointer');
        var uuid = 'id_' + guid();
        span_button.setAttribute('id', uuid);
        span_button.setAttribute('onclick', 'hide_show(id)');


        if (ols[i].hasAttribute('hidden') == true){
            span_button.appendChild(document.createTextNode(' ◀'));
        } else {
            span_button.appendChild(document.createTextNode(' ▽'));
        }

        ols[i].parentElement.insertBefore(span_button, ols[i]);
    }
}
