// Handeling change password modal 

const modal = document.getElementById("modal") ; 
const openBtn =  document.getElementById("open-modal")

openBtn.onclick = function(){
    modal.style.display = "block"
}

const closeBtn = document.getElementById("close-modal")
closeBtn.onclick  = function(){
    modal.style.display ="none"
}