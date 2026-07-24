



//keyboard short cuts for reception buttons 
document.addEventListener("keydown", function (event) {

    switch (event.key) {

        case "F1":
            event.preventDefault();
            document.getElementById("btn-help").click();
            break;

        case "F2":
            event.preventDefault();
            document.getElementById("btn-first").click();
            break;

        case "F3":
            event.preventDefault();
            document.getElementById("btn-list").click();
            break;

        case "F4":
            event.preventDefault();
            document.getElementById("btn-manual").click();
            break;

        // case "F5":
        //     event.preventDefault();
        //     document.getElementById("btn-clothes").click();
        //     break;

        case "F6":
            event.preventDefault();
            document.getElementById("btn-clear").click();
            break;

        case "Escape":
            event.preventDefault();
            history.back();
            break;
    }

});





