//script file => create_course page 

const form = document.querySelector("form");

const progress =
document.getElementById("progress-container");

const bar =
document.getElementById("progress-bar");


form.addEventListener("submit", function(e){

    e.preventDefault(); // جلوگیری از ارسال فوری فرم


    progress.style.display="block";


    let value = 0;


    let timer=setInterval(()=>{


        if(value < 90){

            value += 10;

            bar.style.width=value+"%";

            bar.innerHTML=value+"%";

        }


    },500);



    setTimeout(()=>{

        clearInterval(timer);

        bar.style.width="100%";

        bar.innerHTML="100%";


        form.submit();


    },5000);


});