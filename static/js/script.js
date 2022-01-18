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
function registrationClient(){
    document.getElementById("client-registration-form");
    document.getElementById("client-registration-form-hidden").hidden = false;
    document.getElementById("service-registration-form-hidden").hidden = true;
    }
function registrationService(){
    document.getElementById("service-registration-form");
    document.getElementById("service-registration-form-hidden").hidden = false;
    document.getElementById("client-registration-form-hidden").hidden = true;
    }
    


//http://127.0.0.1:5000/services
