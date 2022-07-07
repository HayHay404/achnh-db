let carousel = document?.getElementById("carousel")
const uploadBtn : any = document.getElementById("upload-btn")
document?.addEventListener("change", (event : Event) => fillCarousel(event))

function fillCarousel(event : Event) {
    const files = uploadBtn?.files

    console.log(files)

    if (carousel.hasChildNodes) {
        removeAllChildNodes(carousel)
    }
    
    for (const file of files) {
        const img = document.createElement("div")
        img.className += "carousel-item w-1/2 max-w-md"
        const imgUrl = URL.createObjectURL(file)
        img.innerHTML = `<img src=${imgUrl}></img>`
        carousel?.appendChild(img)
    }
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}