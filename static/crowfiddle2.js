class Loader {
    search_input_id = "load_value";
    search_button_id = "load_button";
}

function sanitize(string) {
    const map = {
        '&': '_',
        '<': '_',
        '>': '_',
        '"': '_',
        "'": '_',
        "/": '_',
    };
    const reg = /[&<>"'/]/ig;
    return string.replace(reg, (match)=>(map[match]));
  }

var loader = new Loader();
var search_input = document.getElementById(loader.search_input_id);
var search_button = document.getElementById(loader.search_button_id);
search_button.onclick = function() {
    let path = "/?filename=";
    let value = sanitize(search_input.value);
    window.location.href = path + value;
}