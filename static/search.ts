let searchBar = document.querySelector("#search-bar")
searchBar?.addEventListener("keydown", (event : any) => {
    if (event.key === "Enter") {
        event.preventDefault()

        let searchFormData = new FormData(document.getElementById("search-form") as HTMLFormElement)
        const accountQuery = searchFormData.get("query")

        // console.log(accountQuery)

        window.location.replace(`/u/${accountQuery}/`)
    }
})
