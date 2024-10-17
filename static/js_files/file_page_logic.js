
$(document).ready(function() {

    var socketio = io.connect("http://127.0.0.1:8000")

    socketio.on("connect", function() {
        socketio.emit("get_html_data", { "search_query": "", "sort_by": "alphabetical" })// gets all the html data
    })

    $("#file_upload").change(function(data) { // on the file upload button is pressed, get, the file data
        var file = data.target.files[0]
        socketio.emit("send_file", { "file_name": file.name, "file_content": file, "username": sessionStorage.getItem("username"), "privilege": sessionStorage.getItem("privilege") })
    });

    socketio.on("alter_html_data", function(data) { // changes the data of the file list if there has been an update to the files

        var final_data = ``

        for (let file of data) {
            final_data += `<div id = ${file["id"]}><input type="checkbox" name="file_checkbox" value=${file["id"]}>
                <h3>${file["file_name"]}</h3>
                <p><b>By ${file["username"]} at ${file["datetime"]}</b></p>
                <hr class="hr_tag">
                </div>
                `
        }

        $("#file_data").html(final_data) // updates the file details
    })

    $("#download_button").on("click", function() { // on the download button being pressed, we get all the files that have been selected

        let selected_id_list = []

        $.each($("input[name='file_checkbox']:checked"), function() {
            selected_id_list.push($(this).val());
            $(this).prop("checked", false);

        });

        socketio.emit("download_or_delete_by_id", { "command": "download", "id_list": selected_id_list })
    })

    $("#delete_button").on("click", function() { // deletes all the selected files 

        let selected_id_list = []

        $.each($("input[name='file_checkbox']:checked"), function() {
            selected_id_list.push($(this).val());
            $(this).prop("checked", false);
        });

        socketio.emit("download_or_delete_by_id", { "command": "delete", "id_list": selected_id_list })
    })

    socketio.on("delete_file_data", function(data) {

        $(`#${data}`).remove() // removes the certain files with the id 

    })

    socketio.on("show_file_data_temp", function(data) {


        var file_data = `<div id = ${data["id"]}><input type="checkbox" name="file_checkbox" value=${data["id"]}>
                <h3>${data["file_name"]}</h3>
                <p><b>By ${data["username"]} at ${data["datetime"]}</b></p>
                <hr class="hr_tag">
                </div>
                `

        $("#file_data").append(file_data)


    })

    $("#search_button").on("click", function() { // when you search, sends everything in the textbox

        var sort_by_val = ``

        if ($('input[name=sort_by]:checked').val() == "sort_alphabetical") {
            sort_by_val = "alphabetical"
        }

        else if ($('input[name=sort_by]:checked').val() == "sort_reverse_alphabetical") {
            sort_by_val = "reverse_alphabetical"
        }

        else if ($('input[name=sort_by]:checked').val() == "sort_datetime") {
            sort_by_val = "datetime"
        }

        var search_value = $("#search_bar").val()

        $("#search_bar").val("")

        socketio.emit("get_html_data", { "search_query": search_value, "sort_by": sort_by_val })

    })

    socketio.on('redirect', function(data) { // redirects the user, based on data
        window.location = data["url"];
    });


})
