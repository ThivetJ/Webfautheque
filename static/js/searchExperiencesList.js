const searchField= document.querySelector("#searchField")
const pagination = document.querySelector(".pagination");
const paginationSearch = document.querySelector(".paginationSearch")
const noResults = document.querySelector(".no-results");
const appTable = document.querySelector(".list");
const ListExperience = document.querySelector(".list_experiences");
const NoResultsText = document.querySelector(".no_result_text");
const obj_per_page = 5;
const option_button = document.querySelector(".option_button").value;
let current_page = 1;
ListExperience.style.display = "none";
if(document.querySelector("#role_modification") === null){
    role_modification =0;
}
else{
     role_modification = document.querySelector("#role_modification").value 
}
if(document.querySelector("#role_suppresion") === null){
    role_suppresion =0;
}
else{
     role_suppresion = document.querySelector("#role_suppresion").value 
}

//range les experiences dans différents tableaux en fonction d'element par page 'chunkSize'
function sliceIntoPages(array, chunkSize) {
    var results = [];
    while (array.length) {
        results.push(array.splice(0, chunkSize));
    }
    return results;
}

//interaction avec les boutons de pagination d'un filtre de recherche
function searchPage(page, dataslice) {
    document.getElementsByClassName('list_experiences')[0].innerHTML = '';
    document.getElementsByClassName('paginationSearch')[0].innerHTML ='';

    if(page === 0){
        current_page = 1;
    }
    else if (page  > dataslice.length) {
        current_page;
    }
    else{
        current_page = page;
    }   
    div = `
    <table id="tab_experience">
    <thead>
        <tr>
            <th>Code</th>
            <th>Date</th>
            <th>Auteur</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
    `;
    dataslice[current_page-1].forEach(experience => {
        const date = new Date(experience.experience_pub_date);
        const date_fr = date.toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        const dtimeHours = date.getHours();
        const dtimeMinutes = date.getMinutes();
        const time = `${dtimeHours < 10 ? '0' : ''}${dtimeHours}:${dtimeMinutes  < 10 ? '0' : ''}${dtimeMinutes}`;
        div+= `
          <tr>
            <td>${experience.experience_nom_article}</td>
            <td>${date_fr + ' '+ time}</td>
            <td>${experience.experience_auteur}</td>
            <td class="bouton_action">
            <div class="add_experience">
                <div class="option_button">
                  <a href="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }"> <button type="submit" aria-label="voir" class="fa-solid fa-eye" name="choice_experience"></button></a>
                </div>
            </div>
            </td>
          </tr>
        `

    });
    document.getElementsByClassName('list_experiences')[0].innerHTML +=div;
    searchDiv =` <span class="current"> Page ${current_page } sur ${pageNumber}  <br>
    </span> `
// for (let i = 1; i <= pageNumber -1; i++) {
//     //searchDiv+= `<a href="?pages=${i}&name=${searchValue}" class="page" onclick="searchPage(${i})">${i}</a>`
//     //use on action to change page
//     searchDiv+= `
//     <a href="#" class="page" onclick="searchPage(${i}, datas)">${i}</a>  `
// }

searchDiv =` <span class="current"> Page ${current_page } sur ${pageNumber}  <br>
    </span>      <br>  
    <span class="step-links">  
    <a href="#" class="page" onclick="searchPage(0, datas)">1</a>  
    <a href="#" class="page" onclick="searchPage(${current_page -1}, datas)">précédent</a>  
    <a href="#" class="page" onclick="searchPage(${current_page +1}, datas)">suivant</a>  
    <a href="#" class="page" onclick="searchPage(${pageNumber}, datas)">${pageNumber }</a>  
    `
document.getElementsByClassName('paginationSearch')[0].innerHTML +=searchDiv;

}


//action lors de la recherche depuis le champ de recherche
searchField.addEventListener('keyup', (e)=>{

    const searchValue = e.target.value;
    //si le champs de recherche n'est pas vide, on lance la requete ajax
    if (searchValue.trim().length > 0) {
        pagination.style.display = "none";
        fetch('/experiences/search_experiences', {
            method: 'POST',
                body: JSON.stringify({searchValue})
                })
                .then(res => res.json())    
                .then(data => { 
                    //aucune experience trouvée
                    if(data.length === 0 ){
                        NoResultsText.style.display = "block"
                        noResults.style.display = "block";
                        ListExperience.style.display = "none";
                        appTable.style.display = "none";

                      }
                    else {
                        paginationSearch.style.display = "block";
                        pageNumber = Math.ceil(data.length / obj_per_page); 
                        datas = sliceIntoPages(data, obj_per_page);
                        appTable.style.display = "none";
                        ListExperience.style.display = "flex";
                        noResults.style.display = "none";
                        document.getElementsByClassName('list_experiences')[0].innerHTML = '';
                        div= `       
               
                        <table id="tab_experience">
                        <thead>
                          <tr>
                            <th>Code</th>
                            <th>Date</th>
                            <th>Auteur</th>
                            <th>Action</th>             
                          </tr>
                        </thead>
                        <tbody> `
                    datas[current_page-1].forEach(experience => {
                        const date = new Date(experience.experience_pub_date);
                        const date_fr = date.toLocaleDateString('fr-FR', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        });
                        const dtimeHours = date.getHours();
                        const dtimeMinutes = date.getMinutes();
                        const time = `${dtimeHours < 10 ? '0' : ''}${dtimeHours}:${dtimeMinutes < 10 ? '0' : ''}${dtimeMinutes}`;
                        document.getElementsByClassName('paginationSearch')[0].innerHTML ='';

                        div+= `
                          <tr>
                            <td>${experience.experience_nom_article}</td>
                            <td>${ date_fr } ${ time }</td>
                            <td>${experience.experience_auteur}</td>
                            <td class="bouton_action">
                            <div class="add_experience">
                                <div class="option_button">
                                  <a href="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }"> <button type="submit" aria-label="voir" class="fa-solid fa-eye" name="choice_experience"></button></a> 
                                  `
                        
                                  if(role_modification){
     
                                    div+= `<form action="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }/Update/">
                         
                                        <button type="submit" aria-label="modifier" class="fa-solid fa-pen-to-square" name="choice_experience"></button>
                                        </form>`
                                    }
                                   if(role_suppresion){
     
                                    div+= ` <form action="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }/Delete/" method="POST">

                                                 
                                    <button type="submit" aria-label="supprimer" class="fa-solid fa-trash-can" name="choice_experience" onClick="return confirm('Voulez Vous supprimer l\'experience {{experience.experience_nom_article}}')"></button>
                                    <input type="hidden" name="next" value="/Webfautheque/experiences" class="hidden_button">
                                        </form>`
                                     }                                                         


                                    div+= `
                              </div>
                          </div>
                        </td>
                          </tr>
                        `



                        
                        document.onclick = function(e){
                            if(e.target.className === 'fa-solid fa-trash-can'){
                                return confirm('Voulez Vous supprimer l\'experience');    
                            }
                        }

                    });
                    div += `</tbody> </table>`
                    searchDiv =` <span class="current"> Page ${current_page} sur ${pageNumber}  <br>
                        </span>      <br>  
                        <span class="step-links">  
                        <a href="#" class="page" onclick="searchPage(0, datas)">1</a>  
                        <a href="#" class="page" onclick="searchPage(${current_page -1}, datas)">précédent</a>  
                        <a href="#" class="page" onclick="searchPage(${current_page +1}, datas)">suivant</a>  
                        <a href="#" class="page" onclick="searchPage(${pageNumber}, datas)">${pageNumber}</a>  
                        `

                    document.getElementsByClassName('paginationSearch')[0].innerHTML +=searchDiv;

                    document.getElementsByClassName('list_experiences')[0].innerHTML +=div;
                    div= `
                    </br>  ` 
                    document.getElementsByClassName('list_experiences')[0].innerHTML +=div;

                }
            })
    }   

    //si le champs de recherche est vide, on affiche la liste des experiences
    else{
        current_page = 1;  
        ListExperience.style.display = "none";
        appTable.style.display = "flex";
        pagination.style.display = "block";
        paginationSearch.style.display = "none";
        NoResultsText.style.display = "none"
        
    }
})
