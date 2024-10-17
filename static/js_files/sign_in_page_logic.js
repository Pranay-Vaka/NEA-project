$(document).ready(function() {

    var socketio = io.connect("http://127.0.0.1:8000")

    let public_key = 0;
    let prime_product = 0;

    socketio.on("update_credentials", function(data) {
        sessionStorage.setItem("username", data["username"])
        sessionStorage.setItem("privilege", data["privilege"])
    })


    socketio.on("connect", function() {
        socketio.emit("get_encryption_key") // gets the encryption keys 
    })

    $("#submit_button").on("click", function() { // take the values for the username and password, while encrypting them
        socketio.emit("handle_credentials", { "username": encrypt(public_key, prime_product, $("#username").val()), "password": encrypt(public_key, prime_product, $("#password").val()) })
        $("#username").val("");
        $("#password").val("");
    })

    socketio.on("save_encryption_key", function(data) { // saves the encryptoin keys
        public_key = data["public_key"]
        prime_product = data["prime_product"]
    })

    socketio.on("error_handler", function(error_message) { // html alert box depending or error

        if (error_message == "wrong_password") {
            alert("Wrong password")

        }

        else if (error_message == "wrong_username") {
            alert("Wrong username")
        }

        else if (error_message == "empty") {
            alert("Empty fields")
        }
    });


    $("#register_button").on("click", function() { // on the register button, takes all the username and password while encrypting them

        console.log({ "username": encrypt(public_key, prime_product, $("#register_username").val()), "password": encrypt(public_key, prime_product, $("#register_password").val()) })

        socketio.emit("handle_register", { "username": encrypt(public_key, prime_product, $("#register_username").val()), "password": encrypt(public_key, prime_product, $("#register_password").val()) })
        $("#register_username").val("");
        $("#register_password").val("");
    })


    socketio.on("register_error_handler", function(error_message) { // on certain errors, the corresponding alert box is sent

        if (error_message == "empty") {
            alert("Empty fields")
            //$("#register_error_message").text("Empty fields")
        }

        else if (error_message == "not_enough_characters") {
            alert("Less than 5 characters used")
            //$("#register_error_message").text("Empty fields")
        }

        else if (error_message == "too_many_characters") {
            alert("More than 18 characters in the fields")
            //$("#register_error_message").text("Empty fields")
        }

        else if (error_message == "queue_full") {
            alert("Too many people registering at once, please try again later")
        }

        else if (error_message == "banned_characters") {
            alert("Using characters that are banned")
        }

        else if (error_message == "username_in_queue") {
            alert("The username is already in the queue")
        }

        else if (error_message == "username_in_database") {
            alert("The user already exists")
        }

        else if (error_message == "successful") {
            alert("Successfully been put into the register queue")
        }


    });

    socketio.on('redirect', function(data) {
        window.location = data["url"];
    });


})

