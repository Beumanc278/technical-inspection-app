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

// helper object for the API interaction
class APIHelper {
    constructor() {
        this.domain = "http://127.0.0.1:5000"
        this.credentials = 'same-origin';
        this.car = Object.create(new baseEntity(this.domain, '/car'));
        this.user = Object.create(new baseEntity(this.domain, '/user'));
        this.service = Object.create(new baseEntity(this.domain, '/service'));
        this.inspection = Object.create(new baseEntity(this.domain, '/inspection'))

        // test functions using for getting all elements
        this.get_all = function (endpoint) {
            return sendRequest("GET", this.domain, endpoint)
        }
    }
}
// base object for each entity in API
class baseEntity {
    constructor(domain, endpoint) {
        this.endpoint = endpoint;
        this.get_example_of_request_body = function () { // only for development purposes, must be deleted
            var result = sendRequest("GET", domain, this.endpoint); 
            return result['fields-for-request'] 
        }
        this.get_by_parameters = function (parameters) {
            var result = sendRequest("POST", domain, this.endpoint, parameters);
            return result[mapping[endpoint]]
        };
        this.insert = function (parameters) {
            return sendRequest("PUT", domain, this.endpoint, parameters);
        };
        this.update = function (parameters) {
            var id_key = Object.keys(parameters)[0];
            if (parameters[id_key] !== null) {
                return sendRequest("PUT", domain, this.endpoint, parameters);
            } else {
                throw "It is prohibited to send request without ID for updating value"
            }
        };
        this.delete = function (parameters) {
            return sendRequest("DELETE", domain, this.endpoint, parameters)
        };
    }
}

// endpoint - list mapping
var mapping = {
    '/car': 'cars',
    '/user': 'users',
    '/service': 'services',
    '/inspection': 'inspections'
}


// function for sending requests
function sendRequest(method, domain, endpoint, parameters = null) {
    var Http = new XMLHttpRequest();
    Http.open(method, domain + endpoint, false);
    Http.setRequestHeader("Access-Control-Allow-Origin", domain);
    Http.setRequestHeader("Accept", "application/json");
    Http.setRequestHeader("Content-Type", "application/json");
    if (method == "GET") {
        Http.send();
    } else if (method == "DELETE") {
        request_body = JSON.stringify(parameters);
        Http.send(request_body);
        if (Http.status == 204) {
            console.log('The item was deleted successfully.')
            return
        }
    } else {
        request_body = JSON.stringify(parameters);
        Http.send(request_body);
    }
    return JSON.parse(Http.responseText)
}