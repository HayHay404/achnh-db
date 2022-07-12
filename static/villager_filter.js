const filterVillager = document.getElementById("villager-filter");
filterVillager.addEventListener("input", (event) => filterSearch(event));
const table = document.getElementById("villager-table");
const tableRow = document.getElementsByTagName("tr");
const checkbox = document.querySelectorAll(".checkbox");
checkbox.forEach((element) => {
    console.log(element.value);
    element.addEventListener("change", (event) => maxSelect(event));
});
function filterSearch(event) {
    for (let i = 0; i < tableRow.length; i++) {
        let td = tableRow[i].getElementsByTagName("td")[0];
        if (td) {
            const txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filterVillager.value.toUpperCase()) > -1) {
                tableRow[i].style.display = "";
            }
            else {
                tableRow[i].style.display = "none";
            }
        }
    }
}
function maxSelect(event) {
    let target = event.target;
    console.log(target.value);
}
