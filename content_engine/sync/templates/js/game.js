var load = function() {
    var image1 = document.getElementById("screenshot_1");
    var image2 = document.getElementById("screenshot_2");
    var image3 = document.getElementById("screenshot_3");
    var image4 = document.getElementById("screenshot_4");
    var img1 = new Image();
    var img2 = new Image();
    var img3 = new Image();
    var img4 = new Image();
    var container = document.getElementById("container");
    img1.src = image1.src;
    img2.src = image2.src;
    img3.src = image3.src;
    img4.src = image4.src;

    if(img1.width > img1.height){
        container.className = "landscape";
    } else {
        container.className = "portrait";
    }
};