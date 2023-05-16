setInterval(check_if_img_loaded, 2000)


function check_if_img_loaded(params) {
    var images = document.images;
    var filteredImages = Array.prototype.filter.call(images, function (img) {
        return img.className.includes("static/img");
    });
    if (filteredImages[0].className != filteredImages[0].name) {
        console.log("diaoyong");
        console.log('classname', filteredImages[0].className)
        console.log('name', filteredImages[0].name)
        preload(filteredImages, 0)
    }
}


function preload(images, index) {
    console.log('preload........................................................................' + index)
    index = index || 0;
    if (images && images.length > index) {
        var img = images[index];
        var src = images[index].className;
        if (index == 0) {
            for (var i = index + 1; i < images.length; i++) {
                console.log('...' + i + '...')
                images[i].onload = null
                images[i].src = 'assets/Russian-Cute-Sexy-Girl.jpg';
            }
        }
        img.onload = function () {
            preload(images, index + 1);
        };
        img.onerror = function () {
            console.log('图片载入失败了...')
            img.src = 'https://a.thumbs.redditmedia.com/UlK91vWguosDZwdVMaMRBRM6dWk7a3Eqn0jcYMnfxp4.png';
            console.log('图片已替换，等待重载入...')
            setTimeout(function () {
                img.src = src;
            }, 180000);
            console.log('图片已载入...')
        }
        img.src = src;
        img.name = src;
    }
}
