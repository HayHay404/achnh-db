const user_image = document.getElementById("user_image");
let image_preview = document.getElementById("profile_image_preview");
user_image.addEventListener("change", (event) => addProfilePreview(event));
// user_image.addEventListener("load", (event : Event) => addProfilePreview(event))
function addProfilePreview(event) {
    let response = fetch(`http://acnhapi.com/v1/villagers/${user_image.value}`).then(async (response) => {
        const response_json = await response.json();
        // console.log(response_json)
        image_preview.src = response_json["icon_uri"];
    });
}
