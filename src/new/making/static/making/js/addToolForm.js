function addForm() {
    // get current amount of forms
    var form_idx = document.querySelector('#id_form-TOTAL_FORMS').value;
    // get max number of forms
    var max_num = document.querySelector('#id_form-MAX_NUM_FORMS').value;
    // only add new form if less than max_forms 
    if (form_idx < max_num) {
        // get the html of the empty form + change prefix to next form index
        var test = document.getElementById('empty_form').innerHTML.replace(/__prefix__/g, form_idx);
        // place this new form at the end of the formset
        document.querySelector('#form_set').insertAdjacentHTML("beforeend", test);
        // increment the total forms counter
        document.querySelector('#id_form-TOTAL_FORMS').value = parseInt(form_idx)+1;
    } 
}   

function deleteForm() {
    // get current amount of forms
    var form_idx = document.querySelector('#id_form-TOTAL_FORMS').value; 
    // only delete if there's 1 or more form 
    if (form_idx >= 1) {
        // go find the 2nd last form (not the empty form)
        var all_forms = document.querySelectorAll(".no_error")
        var form = all_forms[all_forms.length - 2]
        form.remove()
        document.querySelector('#id_form-TOTAL_FORMS').value = parseInt(form_idx)-1;
    }
}




  