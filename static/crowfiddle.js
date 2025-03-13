class CreateNewFile {
    input_table_id = "create_table_form";
    input_button_add_id = "create_table_add_column";
    input_button_remove_id = "create_table_remove_column";
    rowCount=1;
}

var createNewFile = new CreateNewFile();
let add_button = document.getElementById(createNewFile.input_button_add_id);
let remove_button = document.getElementById(createNewFile.input_button_remove_id);
add_button.onclick = function() {
    createNewFile.rowCount += 1;
    let table = document.getElementById(createNewFile.input_table_id);
    let row = table.insertRow(createNewFile.rowCount);
    row.insertCell(0).outerHTML = "<th>Column "+createNewFile.rowCount+"</th>";
    let cell2 = row.insertCell();
    cell2.innerHTML = "<input name=\"col-"+createNewFile.rowCount+"\" id=\"col-"+createNewFile.rowCount+"\" required placeholder=\"Name of column\">";
};
remove_button.onclick = function() {
    let table = document.getElementById(createNewFile.input_table_id);
    if (createNewFile.rowCount > 1) {
        table.deleteRow(createNewFile.rowCount)
    }
    createNewFile.rowCount -= 1;
}