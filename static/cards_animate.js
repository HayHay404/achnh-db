const all_cards = document.querySelectorAll(".card")
const all_paras = document.querySelectorAll("p")

for (card of all_cards) {
    card.velocity("fadeIn", {duration: 1500 });
}

for (para of all_paras) {
    para.velocity("fadeIn", {duration: 1500});
}