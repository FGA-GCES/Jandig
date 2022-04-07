var THREEx = THREEx || {}

THREEx.ArPatternFile = {}

THREEx.ArPatternFile.toCanvas = function(patternFileString, onComplete) {
    console.assert(false, 'not yet implemented')
}

//////////////////////////////////////////////////////////////////////////////
//		function to encode image
//////////////////////////////////////////////////////////////////////////////

THREEx.ArPatternFile.encodeImageURL = function(imageURL, onComplete) {
    var image = new Image;
    image.onload = function() {
        var patternFileString = THREEx.ArPatternFile.encodeImage(image)
        onComplete(patternFileString)
    }
    image.src = imageURL;
}

THREEx.ArPatternFile.encodeImage = function(image) {
    // copy image on canvas
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d')
    canvas.width = 16;
    canvas.height = 16;


    var patternFileString = ''
    for (var orientation = 0; orientation > -2 * Math.PI; orientation -= Math.PI / 2) {
        // draw on canvas - honor orientation
        context.save();
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.translate(canvas.width / 2, canvas.height / 2);
        context.rotate(orientation);
        context.drawImage(image, -canvas.width / 2, -canvas.height / 2, canvas.width, canvas.height);
        context.restore();

        // get imageData
        var imageData = context.getImageData(0, 0, canvas.width, canvas.height)

        // generate the patternFileString for this orientation
        if (orientation !== 0) patternFileString += '\n'
            // NOTE bgr order and not rgb!!! so from 2 to 0
        for (var channelOffset = 2; channelOffset >= 0; channelOffset--) {
            for (var y = 0; y < imageData.height; y++) {
                for (var x = 0; x < imageData.width; x++) {

                    if (x !== 0) patternFileString += ' '

                    var offset = (y * imageData.width * 4) + (x * 4) + channelOffset
                    var value = imageData.data[offset]

                    patternFileString += String(value).padStart(3);
                }
                patternFileString += '\n'
            }
        }
    }

    return patternFileString
}

//////////////////////////////////////////////////////////////////////////////
//		trigger download
//////////////////////////////////////////////////////////////////////////////

THREEx.ArPatternFile.triggerDownload = function(patternFileString) {
    // tech from https://stackoverflow.com/questions/3665115/create-a-file-in-memory-for-user-to-download-not-through-server
    var domElement = window.document.createElement('a');
    domElement.href = window.URL.createObjectURL(new Blob([patternFileString], { type: 'text/plain' }));
    domElement.download = 'pattern-marker.patt';
    document.body.appendChild(domElement)
    domElement.click();
    document.body.removeChild(domElement)
}

THREEx.ArPatternFile.buildFullMarker = function (innerImageURL, pattRatio, onComplete) {
    const whiteMargin = 0.1
    const blackMargin = (1 - 2 * whiteMargin) * ((1 - pattRatio) / 2)
    const innerMargin = whiteMargin + blackMargin

    let canvas = document.createElement('canvas');
    let context = canvas.getContext('2d')
    canvas.width = canvas.height = 512

    context.fillStyle = 'white';
    context.fillRect(0, 0, canvas.width, canvas.height)

    copyImageOnCanvas({
        currentCanvas: canvas,
        canvasContext: context,
        whiteMargin
    })

    clearInnerImageArea({
        currentCanvas: canvas,
        canvasContext: context,
        innerMargin
    })
    
    let innerImage = document.createElement('img')
    innerImage.addEventListener('load', drawInnerImage({
        currentCanvas: canvas,
        canvasContext: context,
        innerMargin,
        imageToDraw: innerImage,
        onCompleteCallback: onComplete
    }))

    innerImage.src = innerImageURL
}

const copyImageOnCanvas = ({ currentCanvas, canvasContext, whiteMargin }) => {
    canvasContext.fillStyle = 'black';
    canvasContext.fillRect(
        whiteMargin * currentCanvas.width,
        whiteMargin * currentCanvas.height,
        currentCanvas.width * (1 - 2 * whiteMargin),
        currentCanvas.height * (1 - 2 * whiteMargin)
    );
}

const clearInnerImageArea = ({ currentCanvas, canvasContext, innerMargin }) => {
    canvasContext.fillStyle = 'white';
    canvasContext.fillRect(
        innerMargin * currentCanvas.width,
        innerMargin * currentCanvas.height,
        currentCanvas.width * (1 - 2 * innerMargin),
        currentCanvas.height * (1 - 2 * innerMargin)
    );
}

const drawInnerImage = ({ currentCanvas, canvasContext, innerMargin, imageToDraw, onCompleteCallback }) => {
      canvasContext.drawImage(imageToDraw,
        innerMargin * currentCanvas.width,
        innerMargin * currentCanvas.height,
        currentCanvas.width * (1 - 2 * innerMargin),
        currentCanvas.height * (1 - 2 * innerMargin)
    );

    const imageUrl = canvas.toDataURL()
    onCompleteCallback(imageUrl)
}