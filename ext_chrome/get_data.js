function text(document){
    var contents = document.body.innerText;
    console.log(contents)

    var sentences = contents.split("\n");
    var sentencesout = sentences.filter(sentence => (sentence.length > 15 && /[^\w\s]/.test(sentence)));
    var sentences = sentencesout.join(". ");
    return sentences
}


