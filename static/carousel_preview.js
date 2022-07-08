let carousel = document?.getElementById("carousel");
const uploadBtn = document.getElementById("upload-btn");
document?.addEventListener("change", (event) => fillCarousel(event));
function fillCarousel(event) {
    const files = uploadBtn?.files;
    /* if (carousel.hasChildNodes) {
        removeAllChildNodes(carousel)
    } */
    if (uploadBtn.files.length > (5 - carousel.children.length)) {
        const textNode = document.createElement("p");
        textNode.innerHTML = "Too many images. Delete some or try uploading less.";
        carousel.appendChild(textNode);
        // uploadBtn.files.remo
        return;
    }
    for (const file of files) {
        const img = document.createElement("div");
        img.className += "carousel-item w-1/2 max-w-md";
        const imgUrl = URL.createObjectURL(file);
        img.innerHTML = `<img src=${imgUrl}></img>`;
        carousel?.appendChild(img);
    }
}
function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}
