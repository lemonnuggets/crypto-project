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
    createUserForm.innerHTML = `
        <br/>
        <label for="name">Name</label>
        <input type="text" name="name" id="name">
        </input>
        <br/>
        <label for="privilege_level">Privilege Level</label>
        <input type="number" name="privilege_level" id="privilege_level" min="0" max="5">
        </input>
        <br/>
        <label for="type">Type</label>
        <select name="type" id="type">
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
        </select>
        <br/>
        <input type="submit" value="Create User">
        </input>
    `
    return createUserForm;
};
const deleteUserElement = () => {
    const deleteUserForm = document.createElement("div");
    deleteUserForm.classList.add("delete-user-form");
    deleteUserForm.innerHTML = `
        <br/>
        <label for="public_key">Public Key</label>
        <input type="number" name="public_key" id="public_key">
        </input>
        <br/>
        <label for="private_key">Private Key</label>
        <input type="number" name="private_key" id="private_key">
        </input>
        <br/>
        <input type="submit" value="Delete User">
        </input>
    `
    return deleteUserForm;
};
const diagnoseElement = () => {
    const diagnoseForm = document.createElement("div");
    diagnoseForm.classList.add("diagnose-form");
    diagnoseForm.innerHTML = `
        <br/>
        <label for="doc_public_key">Doctor Public Key</label>
        <input type="number" name="doc_public_key" id="doc_public_key">
        </input>
        <br/>
        <label for="doc_private_key">Doctor Private Key</label>
        <input type="number" name="doc_private_key" id="doc_private_key">
        </input>
        <br/>
        <label for="public_key">Public Key</label>
        <input type="number" name="public_key" id="public_key">
        </input>
        <br/>
        <label for="diagnosis">Diagnosis</label>
        <input type="text" name="diagnosis" id="diagnosis">
        </input>
        <br/>
        <input type="submit" value="Add Diagnosis">
        </input>
    `
    return diagnoseForm;
};
const readElement = () => {
    const readForm = document.createElement("div");
    readForm.classList.add("read-form");
    readForm.innerHTML = `
        <br/>
        <label for="public_key">Public Key</label>
        <input type="number" name="public_key" id="public_key">
        </input>
        <br/>
        <input type="submit" value="Read Records">
        </input>
    `
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
