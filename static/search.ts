let searchBar = document.querySelector("#search-bar")
searchBar?.addEventListener("submit", (event : Event) => {
    event.preventDefault()
    let url = window.location.href
    console.log(url)
    window.location.replace("")
});

export {};