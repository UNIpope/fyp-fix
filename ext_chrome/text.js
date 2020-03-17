alert("text getting");

var contents = document.body.innerText;
console.log(contents)

var sentences = contents.split("\n");
var sentencesout = sentences.filter(sentence => (sentence.length > 15 && /[^\w\s]/.test(sentence)));
var sentences = sentencesout.join(". ");

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



console.log(sentencesout)
console.log(/[^\w\s]/.test("hello i am i test boi my dude"))
console.log(/[^\w\s]/.test("hello i am i test boi my dude."))
//https://www.breakingnews.ie/world/roman-polanski-to-skip-french-oscars-amid-protests-following-new-rape-claim-984453.html
//Coronavirus                   still in array
//Breaking News                 removed from array