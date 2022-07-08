const user_image : HTMLSelectElement = document.getElementById("user_image") as HTMLSelectElement
let image_preview : HTMLImageElement = document.getElementById("profile_image_preview") as HTMLImageElement
user_image.addEventListener("change", (event : Event) => addProfilePreview(event))
// user_image.addEventListener("load", (event : Event) => addProfilePreview(event))

function addProfilePreview(event : Event) {
    let response = fetch(`http://acnhapi.com/v1/villagers/${user_image.value}`).then(async response => {
        const response_json = await response.json()
        // console.log(response_json)
        image_preview.src = response_json["icon_uri"]
    })
}
