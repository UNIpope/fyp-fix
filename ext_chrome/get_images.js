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


var extp = chrome.runtime.getURL("popup.html")
var ls = extp.getElementById("ads_stats");
ls.append("hi")

/*
for (i = 0; i < images.length; i++) {
    show_image(images[i], 200, 200, i)
} 
*/