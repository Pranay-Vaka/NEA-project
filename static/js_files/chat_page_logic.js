function scroll_to_bottom() {
    $('.chat_container').scrollTop($('.chat_container')[0].scrollHeight)

}


$(document).ready(function() {

    var socketio = io.connect('http://127.0.0.1:8000');


    let public_key = 0;
    let prime_product = 0;

    socketio.on("connect", function() { // gets the encryption keys
        socketio.emit("get_encryption_key")
        socketio.emit("get_messages") // gets the messgages from the room
    });


    socketio.on("handle_messages_from_database", function(data) { // iterates through the html data and creates thta message on the website
        let html_data = ``


        for (let i of data) {
            html_data += `<div class="post_container" id="posts"><h4><b><u>By ${i["username"]} at ${i["datetime"]}</u></b></h4>
                <p>${i["message"]}</p></div><hr class="hr_tag">`

        }

        $(".message_area").html(html_data)
        scroll_to_bottom()

    })


    socketio.on("save_encryption_key", function(data) { // saves the keys
        public_key = data["public_key"]
        prime_product = data["prime_product"]
    })


    $("#send_message").on("click", function() { // on the click of the submit button, the message is sent from the textox
        let encrypted_data = encrypt(public_key, prime_product, $("#message_textarea").val()) // encrypts the data
        $("#message_textarea").val("") // clears the data in the textbox
        socketio.emit("handle_message", { "encrypted_data": encrypted_data, "username": sessionStorage.getItem("username"), "privilege": sessionStorage.getItem("privilege") })
    })


    socketio.on("handle_errors", function(data) { // handles the error messages

        if (data["response_message"] == "full") { alert("Too many characters") }

        else if (data["response_message"] == "empty") { }

    })


    socketio.on("live_update_messages", function(data) { // updates the messages based on the server response

        let html_data = ``

        html_data = `<div class="post_container" id="posts"><h4><b><u>By ${data["username"]} at ${data["datetime"]}</u></b></h4> 
                <p>${data["message"]}</p></div><hr class="hr_tag">`

        $(".message_area").append(html_data) // appends to the html file

        scroll_to_bottom() // scrolls to the botton if there has been an update


    })


})
