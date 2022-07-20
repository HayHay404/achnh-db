let saying = document.getElementById("saying");
let birthday = document.getElementById("birthday");
let personality = document.getElementById("personality");
let hobby = document.getElementById("hobby");
let villager_id = document.querySelector("h1");
async function fillPage() {
    fetch(`http://acnhapi.com/v1/villagers/${villager_id.id}`).then(async (response) => {
        const responseJson = await response.json();
        saying.innerText += " " + responseJson["saying"];
        birthday.innerText += " " + responseJson["birthday-string"];
        personality.innerText += " " + responseJson["personality"];
        hobby.innerText += " " + responseJson["hobby"];
    });
}
fillPage();
