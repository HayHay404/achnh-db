const filterVillager : HTMLInputElement = document.getElementById("villager-filter") as HTMLInputElement
filterVillager.addEventListener("input", (event : Event) => filterSearch(event))
const table : HTMLTableElement = document.getElementById("villager-table") as HTMLTableElement
const tableRow = document.getElementsByTagName("tr")

const checkbox = document.querySelectorAll(".checkbox")
checkbox.forEach((element : HTMLInputElement) => {
    console.log(element.value)
    element.addEventListener("change", (event : InputEvent) => maxSelect(event))
})

function filterSearch(event : Event) {
    for (let i = 0; i < tableRow.length; i++) {
        let td = tableRow[i].getElementsByTagName("td")[0]

        if (td) {
            const txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filterVillager.value.toUpperCase()) > -1) {
                tableRow[i].style.display = "";
            } else {
                tableRow[i].style.display = "none";
            }
        }
    }
}

function maxSelect(event : InputEvent) {
    let target = event.target as any
    console.log(target.value)
}