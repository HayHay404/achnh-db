"use strict";
exports.__esModule = true;
var searchBar = document.querySelector("#search-bar");
searchBar === null || searchBar === void 0 ? void 0 : searchBar.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        var searchFormData = new FormData(document.getElementById("search-form"));
        var accountQuery = searchFormData.get("query");
        window.location.replace("".concat(accountQuery));
    }
});
