var carousel = document === null || document === void 0 ? void 0 : document.getElementById("carousel");
var uploadBtn = document.getElementById("upload-btn");
document === null || document === void 0 ? void 0 : document.addEventListener("change", function (event) { return fillCarousel(event); });
function fillCarousel(event) {
    var files = uploadBtn === null || uploadBtn === void 0 ? void 0 : uploadBtn.files;
    console.log(files);
    if (carousel.hasChildNodes) {
        removeAllChildNodes(carousel);
    }
    for (var _i = 0, files_1 = files; _i < files_1.length; _i++) {
        var file = files_1[_i];
        var img = document.createElement("div");
        img.className += "carousel-item w-1/2 max-w-md";
        var imgUrl = URL.createObjectURL(file);
        img.innerHTML = "<img src=".concat(imgUrl, "></img>");
        carousel === null || carousel === void 0 ? void 0 : carousel.appendChild(img);
    }
}
function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}
