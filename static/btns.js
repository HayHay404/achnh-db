const btn = document.querySelector("#submit");
const upload = document.querySelector("#upload-btn");
btn.addEventListener("click", (evt) => {
    document.forms["img-upload"].submit();
    document.forms["user-info"].submit();
    document.forms["villager-select"].submit();
});
const forms = document.querySelectorAll("form");
forms.forEach((form) => {
    form.addEventListener("submit", (evt) => {
        evt.preventDefault();
    });
});
