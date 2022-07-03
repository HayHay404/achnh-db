"use strict";
exports.__esModule = true;
var searchBar = document.querySelector("#search-bar");
searchBar === null || searchBar === void 0 ? void 0 : searchBar.addEventListener("submit", function (event) {
    event.preventDefault();
    var url = window.location.href;
    console.log(url);
    window.location.replace("");
});
