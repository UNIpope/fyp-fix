function show_image(src, width, height, alt) {
    var img = document.createElement("img");
    img.src = src;
    img.width = width;
    img.height = height;
    img.alt = alt;

    // This next line will just add it to the <body> tag
    extp.body.appendChild(img);
}


alert("stole ya images");
var images = document.images;
alert(images.length)

function tobase64(image, outputFormat){
    var canvas = document.createElement("canvas");
    document.body.appendChild(canvas);

    canvas.width  = image.width;
    canvas.height = image.height;

    var context = canvas.getContext("2d");

    context.drawImage(image, 0, 0);
    datau = canvas.toDataURL(outputFormat)
    console.log('RESULT:', datau)

}

tobase64(images[15])
var images64 = images.f

async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)   
    });
    return await response.json(); // parses JSON response into native JavaScript objects
  }

postData('http://localhost:5000/test', {"image": tobin(images[0]), "hello":"nothin"})
    .then((data) => {
        console.log(data); // JSON data parsed by `response.json()` call
});


/*

for (i = 0; i < images.length; i++) {
    show_image(images[i], 200, 200, i)
} 

var extp = chrome.runtime.getURL("popup.html")
var ls = extp.getElementById("ads_stats");
ls.append("hi")
*/