function selectAllCheckboxes(source) {
    var checkboxes = document.getElementsByName('selected_records');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}
