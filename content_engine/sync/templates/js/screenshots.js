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
    var count = 0;
    if(image1 != null){
    img1.src = image1.src;
    count ++;
    }
    if(image2 != null){
    img2.src = image2.src;
    count ++;
    }
    if(image3 != null){
    img3.src = image3.src;
    count ++;
    }
    if(image4 != null){
    img4.src = image4.src;
    count ++;
    }
    if(img1.width > img1.height){
        container.className = "landscape";
    }
    else if(count == 4) {
        container.className = "portrait4";
    }
    else if(count == 3){
        container.className = "portrait3";
    }
    else if(count == 2){
        container.className = "portrait2";
    }
    else {
        container.className = "portrait1";
    }
};
