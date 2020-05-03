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

function text(document){
    var contents = document.body.innerText;
    var contentsnum = contents.replace(/[0-9]/g, '')
    var sentences = contentsnum.split(".");
    var sentencesout = sentences.filter(sentence => (sentence.length > 17 && /[^\w\s]/.test(sentence)));
    console.log(sentencesout)
    var senassembled = sentencesout.join(". ");

    console.log(senassembled)
    return senassembled
}

alert("grabbing images");

var imageout = [];
var dataout = {};

var images = document.images;
var sentences = text(document);

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

var promises = [];
promises.push(
    postData('http://localhost:5000/w2v', {"content": sentences, "hello":"nothin"})
    .then((data) => {
        console.log(data);
        dataout = {"content":data}
    })
);

Array.prototype.forEach.call(images, image => {
    promises.push(
        postData('http://localhost:5000/image', {"image": tobase64(image)})
        .then((data) => {
            console.log(data);
            imageout.push(data["im"]);      
        })
    )
});

Promise.all(promises).then(values =>{
    dataout["image"] = imageout
    console.log(dataout)
    postData('http://localhost:5000/compare', dataout)
    .then((data) => {
        console.log(data);
        alert(data["out"]);
    })
});
