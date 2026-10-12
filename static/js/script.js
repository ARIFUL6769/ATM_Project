function showPin() {
    const pin = document.getElementById("pin");

    if (pin.type === "password") {
        pin.type = "text";
    } else {
        pin.type = "password";
    }
}