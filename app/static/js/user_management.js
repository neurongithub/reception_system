
    const createUserModal = document.getElementById("create-user-modal");
    const createUserForm = document.querySelector("#create-user-modal form");
    const usernameInput = document.getElementById("create-username");
    const closeModalWindow = document.getElementById("close-create-user-modal")

    document
        .getElementById("open-create-user-modal")
        .addEventListener("click", () => {

            createUserModal.style.display = "flex";
            usernameInput.focus(); 


        });


    document
        .getElementById("create-user-cancel")
        .addEventListener("click", () => {

            createUserForm.reset();

            createUserModal.style.display = "none";

        });


    window.addEventListener("click", (event) => {

        if (event.target === createUserModal) {

            createUserForm.reset();

            createUserModal.style.display = "none";

        }

    });

  
//=============================edit user modal==================================

const editUserModal = document.getElementById("edit-user-modal");

const editButtons = document.querySelectorAll(".edit-btn");


editButtons.forEach((button) => {

    button.addEventListener("click", () => {
        

        // Get user data from data-* attributes

        const userId = button.dataset.userId;
        const username = button.dataset.username;
        const fullName = button.dataset.fullName;
        const role = button.dataset.role;


        // Put user ID into hidden input

        document.getElementById("edit-user-id").value = userId;


        // Put user information into form

        document.getElementById("edit-username").value = username;

        document.getElementById("edit-full-name").value = fullName;

        document.getElementById("edit-role").value = role;


        // Password fields must always be empty

        document.getElementById("edit-password").value = "";

        document.getElementById("edit-confirm-password").value = "";


        // Show modal

        editUserModal.style.display = "flex";

    });

});




document
    .getElementById("close-edit-user-modal")
    .addEventListener("click", () => {

        editUserModal.style.display = "none";

    });




document
    .getElementById("cancel-edit-user")
    .addEventListener("click", () => {

        editUserModal.style.display = "none";

    });


// ==========================================================
// Close Modal - Click Outside
// ==========================================================

window.addEventListener("click", (event) => {

    if (event.target === editUserModal) {

        editUserModal.style.display = "none";

    }

});









    //=============================delete user =====================================

  document.querySelectorAll(".delete-btn").forEach(button => {

    button.addEventListener("click", function () {

        const userId = this.dataset.userId;
        const username = this.dataset.username;

        const confirmed = confirm(
            `آیا از حذف کاربر "${username}" مطمئن هستید؟`
        );

        if (!confirmed)
            return;

        // Create POST Form
        const form = document.createElement("form");

        form.method = "POST";
        form.action = "/dashboard/delete_user/" + userId;

        document.body.appendChild(form);

        form.submit();

    });

});


