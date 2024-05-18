let PeRP_original = document.getElementsByTagName("PeRP");
let PRP_original = document.getElementsByTagName("PRP");
let PRP_ids = [];
let PeRP_ids = [];

for (x in PRP_original){

    PRP_ids.push(PRP_original[x].id)
    PeRP_ids.push(PeRP_original[x].id)
};

console.log(PRP_ids)
