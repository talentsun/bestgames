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
    if(image1 != null){
    img1.src = image1.src;
    }
    if(image2 != null){
    img2.src = image2.src;
    }
    if(image3 != null){
    img3.src = image3.src;
    }
    if(image4 != null){
    img4.src = image4.src;
    }
    if(img1.width > img1.height){
        container.className = "landscape";
    } else {
        container.className = "portrait";
    }
};
