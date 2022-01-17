function sendJSON() {
    var fields = ['car-brend', 'car-model', 'car-year', 'car-engine-type', 'car-engine-capacity', 'car-transmission', 'car-drive-unit']
    var output_request_body = {}
    fields.forEach(function(element) {
    if (document.getElementById(element) !== null) {
        output_request_body[element] = document.getElementById(element).value;
    }
    })
    console.log(JSON.stringify(output_request_body))
}



/*window.onload = function() {
    var car_brend_element = document.getElementById("car-brend");
    console.log(car_brend_element);
    var car_brend_value = car_brend_element.value;
    console.log(car_brend_value);
}*/
//$(function(){
    
   /* function sendJSON(){ 
        var car_brend_value = document.getElementById("car-brend").value;     
        var car_model_value = document.getElementById("car-model").value;
        var car_generation_value = document.getElementById("car-generation").value;
        var car_drive_unit_value = document.getElementById("car-drive-unit").value;
        var car_engine_type_value = document.getElementById("car-engine-type").value;
        var  car_engine_capacity_value = document.getElementById("car-engine-capacity").value;
        var car_transmission_value = document.getElementById("car-transmission").value;
        

        var data = JSON.stringify({
            "car-brend" : car_brend_value,
            "car-model" : car_model_value,
            "car-year" : car_generation_value,
            "car-drive-unit" : car_drive_unit_value,
            "car-engine-type" : car_engine_type_value,
            "car-engine-capacity" : car_engine_capacity_value,
            "car-transmission" : car_transmission_value,
        });
        console.log(data);*/

        
    
        
    
//})

    









//xhr.send(data);

/*$(function(){
	console.log($('#client-info').text());
});

client-form.ob*/