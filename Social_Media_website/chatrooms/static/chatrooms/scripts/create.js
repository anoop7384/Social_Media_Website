console.log("Welcome");

const findMyLoc = () => {
    console.log("Getting the location");
    const status = document.querySelector('#location');
    const success = (position) => {
        
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        //console.log(latitude,longitude);
        const geoAPI_URL= 'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude='+latitude+'&longitude='+longitude+'&localityLanguage=en';

        fetch(geoAPI_URL)
        .then(res => res.json())
        .then(data => {
            console.log(data);
            status.textContent= data.locality +' , '+ data.principalSubdivision +' , '+data.countryName;
        })
    }
    const error = () => {
        status.textContent = "Unable to retrieve your location"
    }


    navigator.geolocation.getCurrentPosition(success, error);
}
document.querySelector('#location').addEventListener('click', findMyLoc);
