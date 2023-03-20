### make.co / makezine
From TOS: "By agreeing to these rights, you allow others to share, redistribute, remix, transform, and build upon your content as long as they provide attribution to you, link to the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license (https://creativecommons.org/licenses/by-nc-sa/4.0/)and identify any changes made to your content." 


Tools: scissors 




### PROJECTS
Title: Wireless LED Kaleidoscope 
Materials: 
Wireless LEDs multicolor, with 5V transmitting coil such as Adafruit 5140
USB power supply, regulated 5V
DC power adapter, screw terminal to female barrel jack Adafruit 368
Adapter cable, male barrel jack to USB plug Adafruit 2697
Painter’s tape or other easily removable tape
Clear acrylic sheet, 1/8″ (3.2mm) thick, 5″×5″ or larger
Mirrored acrylic sheet, 1/8″ (3.2mm) thick, 10″×8″ or larger
Wood or acrylic sheet, 1/8″ (3.2mm) thick, 20″×12″ or larger for the kaleidoscope frame
Machine screws, M3×12mm (10) with nuts
Machine screws, M3×16mm or longer (3) with nuts
Decorative adhesive vinyl, 12″×10″ or larger
Vector design files
Tools:        
Laser cutter or a laser-cutting service like Ponoko
Craft knife and cutting mat
Screwdriver
Scissors
Wire stripper

Steps:
1. Laser cut the parts 
2. Assemble the frame and eyepiece 
3. Prepare and insert the mirrors

_________
<b>Title:</b> mini ground effect vehicle 
<b>Materials:</b>
Paper cardstock such as index cards
Mini binder clips
Small paper clips
Tape
<b>Tools:</b>
Ruler
Pencil
Scissors
<b>Steps:</b>
1. Make the body
    - cut a bit paper to the dimensions
    - fold paper
2. Add the stabiliser 
    - cut a bit of paper to the dimensions
    - fold paper
    - tape it (to itself? to the other bit of paper?)
3. Add clips
    - put some binder clips at the front of it
_____
https://makezine.com/projects/maker-magic-the-card-machine-trick/
<b>Title:</b> Paper Card Machine
<b>Description:</b>
<b>Materials:</b> standard envelope, pencil, 3-4 rubber bands, cards
<b>Tools:</b> scissors (1)
<b>Steps:</b>
[1.] Seal the empty envelope 
[2.] line up a playing card with its short end along the envelopes short side
[3.] Cut envelope about 2cm past the card 
[4.] Turn the envelope so the open end faces up. About ¾” below the open end, cut or tear small half circles on either side
[5.] Decorate envelope 
[6.] Twist and wrap 3-4 rubber bands around the middle of your pencil 
[7.] Carefully push pencil through the holes
[8.] Now, you can put a card on either side of the pencil in the envelope and twist the pencil to reveal each one 
_____
<b>Title:</b>
<b>Materials:</b>
<b>Tools:</b>
<b>Steps:</b>
data.update(Requirements.syl_dict(self.requirements))


## notes
Should probably 


$('#add_more').click(function() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});

<script> document.querySelector('#add_more').click(function() {
	var form_idx = document.querySelector('#id_form-TOTAL_FORMS').value;
	document.querySelector('#form_set').insertAdjacentHTML("beforeend",document.querySelector('#empty_form').html().replace(/__prefix__/g, form_idx));
	document.querySelector('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
}); </script>
<button onclick="myFunction()">Click me!</button> <br>

{{ projects }} <br>
{{ toolFormSet.management_form }}
<div id="form_set">
    {% for form in toolFormSet.forms %}
	    {{form.non_field_errors}}
		{{form.errors}}
        <table class='no_error'>
            {{ form }}
        </table>
    {% endfor %}
</div>
<input type="button" value="Add More" id="add_more">
<div id="empty_form" style="display:none">
    <table class='no_error'>
        {{ toolFormSet.empty_form }}
    </table>
</div>



<form method="post" action="{% url 'making:test_page' %}">
    {% csrf_token %}
    {{ toolFormSet }}

    <input type="submit" name="submit" value="Submit" /> 
</form> <br>
{{ test }}


<script>
    document.querySelector('#delete').addEventListener("click",deleteForm)   
</script>