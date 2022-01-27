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
function addCarForm() {
    if(document.getElementById("client-form").hidden==true){
        document.getElementById("client-form").hidden=false;
    } else document.getElementById("client-form").hidden=true;
}
function regForm(){
    document.getElementById("account-type").hidden = false;
    document.getElementById("buttons-start").hidden = true;
}

function addCarToDatabase() {
    var new_car_parameters = getCarValuesFromPage();
    response = helper.car.insert(new_car_parameters);
    alert(response['message'])
}

function getInspections() {
    car_parameters = getCarValuesFromPage();
    car_ids = getCarIds(car_parameters);
    all_inspections = new Array;
    if (car_ids != null) {
        car_ids.forEach(car_id=> {
            inspections_for_id = helper.inspection.get_by_parameters({"inspection-car-id": car_id})
            all_inspections = all_inspections.concat(inspections_for_id)
        })
        textarea_element = document.getElementById("inspections")
        textarea_text = ""
        all_inspections.forEach(inspection=> {
            service_for_inspection = helper.service.get_by_parameters({"service-id": inspection['inspection-service-id']})[0]
            textarea_text += `Сервис: ${service_for_inspection['service-name']}\nОписание сервиса: ${service_for_inspection['service-description']}\nНаименование ТО: ${inspection['inspection-name']}\nПробег: ${inspection['inspection-mileage']}\nСтоимость: ${inspection['inspection-cost']}\n\n`
        })
        textarea_element.value = textarea_text;
    } else {
        document.getElementById("inspections").value = ""
        alert("No cars were found")
    }
}

function getCarValuesFromPage() {
    var new_car_parameters = helper.car.get_example_of_request_body();
    for (var key in new_car_parameters) {
        if (key !== "car-id") {
            value_from_page = document.getElementById(key).value;
            if (value_from_page == "") {
                new_car_parameters[key] = null;
            } else {
                new_car_parameters[key] = value_from_page;
            }
        }
    }
    return new_car_parameters;
}

function getCarIds(car_parameters) {
    cars = helper.car.get_by_parameters(car_parameters);
    if (cars != undefined) {
        car_ids = new Array();
        cars.forEach(car => {
            car_ids.push(car['car-id']);
        })
        return car_ids;
    } else {
        return null;
    }
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

var helper = new APIHelper();