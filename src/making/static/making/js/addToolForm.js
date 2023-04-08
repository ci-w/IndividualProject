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

// min_val is the minimum number of forms you want displayed. Default is allowing 0 forms displayed.
function deleteForm(min_val=0) {
    // get current amount of forms
    var form_idx = parseInt(document.querySelector('#id_form-TOTAL_FORMS').value); 

    // only delete if there's 1 or more forms than the min_val 
    if (form_idx > min_val) {
        // go find the 2nd last form (not the empty form)
        var all_forms = document.querySelectorAll(".no_error")
        var form = all_forms[all_forms.length - 2]
        form.remove()
        document.querySelector('#id_form-TOTAL_FORMS').value = form_idx-1;
    }
}




  