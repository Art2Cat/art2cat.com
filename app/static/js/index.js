// dynamic set hr width same as subHead width.
function setWidthForHR() {
    var hr = document.getElementById("dynamicHR");
    var subHead = document.getElementById("subHead");
    if (hr !== null && subHead !== null) {
        hr.style.width = (parseInt(subHead.clientWidth, 10) + 5) + "px";
    }
}

setWidthForHR()

function startGame() {
    var x = document.getElementById("content");
    var game = document.getElementById("game");
    var button = document.getElementById("switch");
    if (x.style.display === "none") {
        x.style.display = "block";
        game.style.display = "none";
        document.location.reload();
    } else {
        x.style.display = "none";
        game.style.display = "block";
        button.innerHTML = "Return";
        draw();
    }
}