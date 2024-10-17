$(document).ready(function() {

    var socketio = io.connect("http://127.0.0.1:8000")


    socketio.on("connect", function() {
        socketio.emit("get_requests") // gets all the register requests
    })


    function change_template(data) {

        if (data == "empty") {
            $("#posts").html("<h4>No requests in the queue</h4>") // if the queue is empty, then output this value

        }

        else {
            $("#username").text(data) // otherwise will update with the username
        }
    }

    socketio.on("handle_requests", function(data) { change_template(data) }) // changes the templates based on register requests


    $("#register").on("click", function() { // on register click button, we get the decision for accepted, rejected and if they are a general or admin

        if ($('input[name=decision_choice]:checked').val() == "reject") {

            socketio.emit("update_requests", { "decision": "false", "real_username": sessionStorage.getItem("username"), "real_privilege": sessionStorage.getItem("privilege") })
            socketio.emit("get_requests")

        }

        else {

            if ($('input[name=privilege_choice]:checked').val() == "general") {
                socketio.emit("update_requests", { "decision": "true", "privilege": "general", "real_username": sessionStorage.getItem("username"), "real_privilege": sessionStorage.getItem("privilege") })
                socketio.emit("get_requests")
            }


            else if ($('input[name=privilege_choice]:checked').val() == "admin") {
                socketio.emit("update_requests", { "decision": "true", "privilege": "admin", "real_username": sessionStorage.getItem("username"), "real_privilege": sessionStorage.getItem("privilege") })
                socketio.emit("get_requests")

            }
        }

    })
});

