function checkStatus() {
    const status = document.getElementById("status");

    status.innerHTML = `<span class="status-badge pending">Checking status...</span>`;

    setTimeout(() => {

        const statuses = [
            { text: "Approved ✅", class: "approved" },
            { text: "Under Verification ⏳", class: "pending" },
            { text: "Rejected ❌", class: "rejected" }
        ];

        const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];

        status.innerHTML = `<span class="status-badge ${randomStatus.class}">
                                ${randomStatus.text}
                            </span>`;

    }, 1500);
}


function togglePassword() {
    const password = document.getElementById("adminPassword");
    const icon = document.getElementById("eyeIcon");

    if (password.type === "password") {
        password.type = "text";
        icon.innerText = "🙈";
    } else {
        password.type = "password";
        icon.innerText = "👁️";
    }
}
function sendMessage(button) {
    const status = document.getElementById("contactStatus");

    button.innerText = "Sending...";
    button.disabled = true;

    setTimeout(() => {
        status.innerHTML = "✅ Message Sent Successfully!";
        status.style.color = "lightgreen";
        button.innerText = "Sent";
    }, 1500);
}

function showSuccess(button) {
    button.innerText = "Processing...";
    button.disabled = true;

    setTimeout(() => {
        button.innerText = "Uploaded ✅";
        button.style.background = "#00c851";
    }, 1500);
}
/*function checkStatus() {
    const status = document.getElementById("status");

    status.innerHTML = `<span class="status-badge pending">Checking status...</span>`;

    setTimeout(() => {
        const statuses = [
            { text: "Approved ✅", class: "approved" },
            { text: "Under Verification ⏳", class: "pending" },
            { text: "Rejected ❌", class: "rejected" }
        ];

        const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];

        status.innerHTML = `<span class="status-badge ${randomStatus.class}">
                                ${randomStatus.text}
                            </span>`;

    }, 1500);
}*/


function togglePassword() {
    const password = document.getElementById("adminPassword");
    const icon = document.getElementById("eyeIcon");

    if (password.type === "password") {
        password.type = "text";
        icon.innerText = "🙈";
    } else {
        password.type = "password";
        icon.innerText = "👁️";
    }
}


function sendMessage(button) {
    const status = document.getElementById("contactStatus");

    button.innerText = "Sending...";
    button.disabled = true;

    setTimeout(() => {
        status.innerHTML = "✅ Message Sent Successfully!";
        status.style.color = "lightgreen";
        button.innerText = "Sent";
    }, 1500);
}


function showSuccess(button) {
    button.innerText = "Processing...";
    button.disabled = true;

    setTimeout(() => {
        button.innerText = "Uploaded ✅";
        button.style.background = "#00c851";
    }, 1500);
}
document.getElementById("uploadForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const status = document.getElementById("uploadStatus");
    const button = this.querySelector("button");

    button.innerText = "Uploading...";
    button.disabled = true;

    setTimeout(() => {
        status.innerHTML = "✅ All Documents Uploaded Successfully!";
        status.style.color = "lightgreen";

        button.innerText = "Uploaded ✅";
    }, 2000);
});