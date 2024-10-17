function get_user_credentials() {

    return { "username": sessionStorage.getItem("username"), "privilege": sessionStorage.getItem("privilege") }
}




function redirect_page(url) {
    window.location = url;
}


