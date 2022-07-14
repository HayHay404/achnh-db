const filterVillager = document.getElementById("villager-filter");
filterVillager.addEventListener("input", (event) => filterSearch(event));
const table = document.getElementById("villager-table");
let villagerList = document.getElementById("villager_list");
const checkbox = document.querySelectorAll("input[type='checkbox']");
let values = [];
const tableRow = document.getElementsByTagName("tr");
checkbox.forEach((element) => {
    //console.log(element.value)
    if (villagerList.value.includes(element.value)) {
        element.checked = true;
        //console.log(element.value)
        values.push(element.value);
    }
    element.addEventListener("change", (event) => select(event));
});
villagerList.value = values.toString();
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
function select(event) {
    let target = event.target;
    if (target.checked === true) {
        values.push(target.value);
    }
    else {
        const idx = values.indexOf(target.value);
        // values.splice(idx)
        let newVals = values.filter(e => e !== target.value);
        //console.log(newVals)
        values = newVals;
    }
    blurCheckbox();
    console.log(villagerList.value);
    villagerList.value = values.toString();
    console.log(villagerList.value);
}
function blurCheckbox() {
    if (values.length === 10) {
        checkbox.forEach((element) => {
            if (element.checked !== true) {
                element.disabled = true;
            }
        });
    }
    else {
        checkbox.forEach((element) => {
            // console.log(element.value)
            if (element.checked !== true && element.value != 'on') {
                element.disabled = false;
            }
        });
    }
}
