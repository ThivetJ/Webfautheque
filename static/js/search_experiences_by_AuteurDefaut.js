

document.getElementsByClassName('search_by_name')[0].onchange= function() {
    
    const name = document.getElementById('searchByName').value;
    if (name.trim().length > 0) {

        fetch ('/experiences/'+idDefaut+'/experienceAuteurDefaut', {
            method: 'POST',
                body: JSON.stringify({name})
                })
                .then(res => res.json())
                .then(data => {
                    if(data.length === 0 ){
                        NoResultsText.style.display = "block"
                        noResults.style.display = "block";
                        ListExperience.style.display = "none";
                        appTable.style.display='none';
                        pagination.style.display = "none";
                    }
                    else {
                        appTable.style.display = "none";
                        ListExperience.style.display = "flex";
                        noResults.style.display = "none";
                        pagination.style.display = "none";

                        document.getElementsByClassName('list_experiences')[0].innerHTML = '';
                        div= `
   
                        <table id="customers">
                        <thead>
                            <tr>
                                <th>Code</th>
                                <th>Date</th>
                                <th>Auteur</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody> `
                        data.forEach(experience => {
                            const date = new Date(experience.experience_pub_date);
                            const date_fr = date.toLocaleDateString('fr-FR', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            });
                            const dtimeHours = date.getHours();
                            const dtimeMinutes = date.getMinutes();
                            const time = `${dtimeHours < 10 ? '0' : ''}${dtimeHours}:${dtimeMinutes < 10 ? '0' : ''}${dtimeMinutes}`;
                            div+= `
                            <tr>
                                <td>${experience.experience_nom_article}</td>
                                <td>${ date_fr } ${ time }</td>
                                <td>${experience.experience_auteur}</td>
                                <td class="bouton_action">
                                <div class="add_experience">
                                    <div class="option_button">
                                      <a href="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }"> <button type="submit" class="fa-solid fa-eye" id="choice_experience"></button></a>
                                      <form action="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }/Update/">
                                      <input type="hidden">
                                          <button type="submit" class="fa-solid fa-pen-to-square" id="choice_experience"></button>
                                      </form>
                                      <form action="/Webfautheque/${ experience.defaut_nom }/Experiences/Consultation:${ experience.id }/Delete/" method="POST">
                                      <input type="hidden" name="next" value="/Webfautheque/experiences" class="hidden_button">
                                          <button type="submit" class="fa-solid fa-trash-can" id="choice_experience" onClick="return confirm('Voulez Vous supprimer l\'experience {{experience.experience_nom_article}}')"></button>
                                      </form>
                                  </div>
                              </div>
                            </td>
                              </tr>
                            `
                            document.onclick = function(){
                                if(event.target.className === 'fa-solid fa-trash-can'){
                                    return confirm('Voulez Vous supprimer l\'experience');    
                                }
                            }
                        });
                        div += `</tbody> </table>`
                        document.getElementsByClassName('list_experiences')[0].innerHTML +=div;
                        div= `
                        </ul>  ` 
                        document.getElementsByClassName('list_experiences')[0].innerHTML +=div;
                    }
                })
        }
        else{
            ListExperience.style.display = "none";
            appTable.style.display = "flex";
            pagination.style.display = "block";
            NoResultsText.style.display = "none"
            

}
}
