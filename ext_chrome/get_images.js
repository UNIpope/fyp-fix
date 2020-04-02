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

function text(document){
    var contents = document.body.innerText;
    console.log(contents)

    var sentences = contents.split("\n");
    var sentencesout = sentences.filter(sentence => (sentence.length > 15 && /[^\w\s]/.test(sentence)));
    var sentences = sentencesout.join(". ");
    return sentences
}

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

postData('http://localhost:5000/w2v', {"content": sentences, "hello":"nothin"})
    .then((data) => {
        console.log(data); // JSON data parsed by `response.json()` call
});

