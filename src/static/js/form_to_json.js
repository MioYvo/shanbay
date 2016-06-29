/**
 * Created by mio on 6/29/16.
 */

function getFormData($form) {
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function redirect_to_home($path) {
    window.location = "http://localhost:5555/" + $path;
}
