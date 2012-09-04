var myImage = document.getElementById("mainImage");

var imageArray = ["/static/images/pic2.jpg","/static/images/pic3.jpg","/static/images/pic4.jpg",
				  "/static/images/pic5.jpg","/static/images/pic1.jpg"];
var imageIndex = 0;

function changeImage() {
	myImage.setAttribute("src",imageArray[imageIndex]);
	imageIndex++;
	if (imageIndex >= imageArray.length) {
		imageIndex = 0;
	}
}

setInterval(changeImage,5000);

// setInterval is also in milliseconds
//var intervalHandle =


//window..onload = function(){
//    setInterval(changeImage,5000);
//};
//
//if (document.addEventListener) {
//  document.addEventListener("DOMContentLoaded", init, false);
//}

//if (window.attachEvent) { window.attachEvent('onload', setInterval(changeImage,5000); }
//else if (window.addEventListener) {window.addEventListener('load', setInterval(changeImage,5000), false);}
//else {document.addEventListener('load', setInterval(changeImage,5000), false);}

//myImage.onclick =  function() {
//	clearInterval(intervalHandle);
//};


