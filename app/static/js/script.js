

//real time function to get real time systemm
function updateClock(){

    let now = new Date();

    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();


    hours = String(hours).padStart(2, "0");
    minutes = String(minutes).padStart(2, "0");
    seconds = String(seconds).padStart(2, "0");


    let time =
        `${hours}:${minutes}:${seconds}`;


    document.getElementById("live-time").innerHTML = time;

}


setInterval(updateClock, 1000);


updateClock();