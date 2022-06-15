

document.getElementsByClassName('search_by_defaut')[0].onchange= function() {
    current_page = 1;
    const name = document.getElementById('searchByDefaut').value;
    //si le champs de recherche n'est pas vide, on lance la requete ajax

    if (name.trim().length > 0) {
        url = '/experiences/experienceByDefaut'
        fetch ('/experiences/experienceByDefaut', {
            method: 'POST',
                body: JSON.stringify({name})
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
                        pagination.style.display = "none";

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
                        <tbody>  `
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
                                  `
                                  if(superuser){
   
                                      div+=
                                      `
                                      <a href="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }"> <button type="submit" aria-label="voir" class="fa-solid fa-eye" name="choice_experience"></button></a> 
                                      <form action="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }/Update/">
                           
                                      <button type="submit" aria-label="modifier" class="fa-solid fa-pen-to-square" name="choice_experience"></button>
                                      </form>
                                      <form action="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }/Delete/" method="POST">
  
                                                   
                                      <button type="submit" aria-label="supprimer" class="fa-solid fa-trash-can" name="choice_experience" onClick="return confirm('Voulez Vous supprimer l\'experience {{experience.experience_nom_article}}')"></button>
                                      <input type="hidden" name="next" value="/Webfautheque/experiences" class="hidden_button">
                                          </form>
                                      `
                                  }
                                  else{
                                  div +=`
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
                                </div>`}`
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
                        searchDiv =` <span class="current"> Page ${current_page } sur ${pageNumber}  <br>
                            </span> `
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
                        <br>  ` 
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
}
