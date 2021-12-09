actionElement = document.querySelector("#action");
formElement = document.querySelector(".request-form");
clearFormHtml = formElement.innerHTML;
const clearForm = () => {
    console.log(formElement, formElement.children);
    [...formElement.children].forEach((child) => {
        if (!child.classList.contains("action")) formElement.removeChild(child);
    });
};

// '<label for="action">Select action</label>' +
// '<select name="action" id="action">' +
// '<option value="none">--Select One--</option>' +
// '<option value="create_user">Create User</option>' +
// '<option value="delete_user">Delete User</option>' +
// '<option value="diagnose">Add patient diagnosis</option>' +
// '<option value="read">Read patient history</option>' +
// '</select>'
const createUserElement = () => {
    const createUserForm = document.createElement("div");
    createUserForm.classList.add("create-user-form");
    return createUserForm;
};
const deleteUserElement = () => {
    const deleteUserForm = document.createElement("div");
    deleteUserForm.classList.add("delete-user-form");
    return deleteUserForm;
};
const diagnoseElement = () => {
    const diagnoseForm = document.createElement("div");
    diagnoseForm.classList.add("diagnose-form");
    return diagnoseForm;
};
const readElement = () => {
    const readForm = document.createElement("div");
    readForm.classList.add("read-form");
    return readForm;
};
actionElement.addEventListener("change", (e) => {
    console.log(e.target.value);
    clearForm()
    switch (e.target.value) {
        case 'create_user':
            formElement.appendChild(createUserElement())
            break;
        case 'delete_user':
            formElement.appendChild(deleteUserElement())
            break;
        case 'diagnose':
            formElement.appendChild(diagnoseElement())
            break;
        case 'read':
            formElement.appendChild(readElement())
            break;
        default:
            break;
    }
});
