
    const createUserModal = document.getElementById("create-user-modal");
    const createUserForm = document.querySelector("#create-user-modal form");
    const usernameInput = document.getElementById("username");

    document
        .getElementById("open-create-user-modal")
        .addEventListener("click", () => {

            createUserModal.style.display = "flex";
            usernameInput.focus(); 


        });


    document
        .getElementById("close-create-user-modal")
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



    //==================================================================

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
