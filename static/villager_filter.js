const filterVillager = document.getElementById("villager-filter");
filterVillager.addEventListener("input", (event) => filterSearch(event));
function filterSearch(event) {
    console.log(filterVillager.value);
}
