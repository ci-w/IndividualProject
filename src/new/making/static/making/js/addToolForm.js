function myFunction() {
    alert("Hello from a static file!");
  }

function testFunction() {
    var form_idx = document.querySelector('#id_form-TOTAL_FORMS').value;
    var test = document.getElementById('empty_form').innerHTML;
    var rep = test.replace(/__prefix__/g, form_idx);
    document.querySelector('#form_set').insertAdjacentHTML("beforeend", rep);
    document.querySelector('#id_form-TOTAL_FORMS').value = parseInt(form_idx)+1; 
}

function deleteForm() {
    // get current amount of forms
    var form_idx = document.querySelector('#id_form-TOTAL_FORMS').value; 
    // need to only delete it if theres 3+ forms total (i.e. 1 form + blank form + 1 to be deleted) 
    if (form_idx > 1) {
        // go find the 2nd last form 
        var test = document.querySelectorAll(".no_error")
        var test2 = test[test.length - 2]
        test2.remove()
        document.querySelector('#id_form-TOTAL_FORMS').value = parseInt(form_idx)-1;
    }
}




  