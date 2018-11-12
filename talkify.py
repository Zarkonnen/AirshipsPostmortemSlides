import sys, json

image_suffixes = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
slides = []

with open(sys.argv[1]) as f:
    slide = dict()
    slide["points"] = []
    for l in f:
        l = l[:-1]
        if l.startswith("- "):
            slide["points"].append(l[2:])
        else:
            if "title" in slide:
                slides.append(slide)
                slide = dict()
                slide["points"] = []
            slide["title"] = l
            if any(l.lower().endswith(suffix) for suffix in image_suffixes):
                slide["image"] = l
    if "title" in slide:
        slides.append(slide)
print """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>""",

print slides[0]["title"]

print """</title>
<style>
html {
    cursor: none;
}
body {
    font-family: "Liberation Sans", no-serif;
    background-color: #241711;
    color: white;
}
#image {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
}
#title {
    font-family: Fledermaus;
    color: #f5e474;
    font-size: 700%;
    margin-top: 11vw;
    margin-bottom: 1em;
    margin-left: 15%;
}
#points {
    padding: 0;
    margin: 0;
    width: 70%;
    margin-left: 15%;
    font-size: 400%;
}
#points li {
    list-style: none;
    margin-bottom: 1em;
}
</style>
<script>
var slides =""",

print json.dumps(slides),

print """;
</script>
<script>
var index = 0;
function showSlide() {
    if (slides[index].image) {
        document.getElementById("title").innerHTML = "";
        document.getElementById("image").src = slides[index].image;
        document.getElementById("image").style.display = "block";
    } else {
        document.getElementById("title").innerHTML = slides[index].title;
        document.getElementById("image").style.display = "none";
    }
    document.getElementById("points").innerHTML = slides[index].points.map(function(p) {
        return "<li>" + p + "</li>";
    }).join("");
}

function next() {
    if (index < slides.length - 1) {
        index++;
        showSlide();
    }
}

function prev() {
    if (index > 0) {
        index--;
        showSlide();
    }
}

function keyup(event) {
    if (event.code == "ArrowLeft") {
        prev();
    } else if (event.code == "ArrowRight" || event.code == "Space") {
        next();
    }
}
</script>
</head>
<body onClick="next()" onKeyUp="keyup(event)">
<img id="image">
<div id="title"></div>
<ul id="points"></ul>
<script>
showSlide();
</script>
</body>
</html>
"""
