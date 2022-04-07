var dialogElement = document.querySelector("#dialog-info");

if (!dialogElement.showModal) {
  //    dialogElementPolyfill.registerDialog(dialogElement)
}

dialogElement
  .querySelector(".mdl-dialog__actions button")
  .addEventListener("click", function () {
    dialogElement.close();
  });

var showDialogButton = document.querySelector("#show-info");
showDialogButton.addEventListener("click", function () {
  dialogElement.showModal();
});

var innerImageURL = null;
var fullMarkerURL = null;

innerImageURL =
  "https://raw.githubusercontent.com/memeLab/ARte/master/src/ARte/core/static/markers/gueixa.png";
updateFullMarkerImage();

document
  .querySelector("#buttonDownloadEncoded")
  .addEventListener("click", function () {
    if (innerImageURL === null) {
      alert("upload a file first");
      return;
    }
    console.assert(innerImageURL);
    THREEx.ArPatternFile.encodeImageURL(
      innerImageURL,
      function onComplete(patternFileString) {
        THREEx.ArPatternFile.triggerDownload(patternFileString);
      }
    );
  });

document
  .querySelector("#buttonDownloadFullImage")
  .addEventListener("click", handleDownloadFullImage);

document.querySelector("#fileinput").addEventListener("change", handleFileInput);

function updateFullMarkerImage() {
  var patternRatio = 0.6;
  THREEx.ArPatternFile.buildFullMarker(
    innerImageURL,
    patternRatio,
    function onComplete(markerUrl) {
      fullMarkerURL = markerUrl;

      var fullMarkerImage = document.createElement("img");
      fullMarkerImage.src = fullMarkerURL;

      // put fullMarkerImage into #imageContainer
      var container = document.querySelector("#imageContainer");
      while (container.firstChild) container.removeChild(container.firstChild);
      container.appendChild(fullMarkerImage);
    }
  );
}

//////////////////////////////////////////////////////////////////////////////
//		Handle PDF
//////////////////////////////////////////////////////////////////////////////
document
  .querySelector("#buttonDownloadPDFOnePerPage")
  .addEventListener("click", generatePdfOnePerPage);
document
  .querySelector("#buttonDownloadPDFTwoPerPage")
  .addEventListener("click", generatePdfTwoPerPage);
document
  .querySelector("#buttonDownloadPDFSixPerPage")
  .addEventListener("click", generatePdfSixPerPage);

function generatePdfOnePerPage() {
  var docDefinition = {
    content: [
      {
        image: fullMarkerURL,
        width: 600,
        alignment: "center",
      },
    ],
  };
  pdfMake.createPdf(docDefinition).open();
}

function generatePdfTwoPerPage() {
  const column = {
    image: fullMarkerURL,
    width: 300,
    alignment: "center",
  };
  var docDefinition = {
    content: [column, column],
  };
  pdfMake.createPdf(docDefinition).open();
}

function generatePdfSixPerPage() {
  const column = {
    image: fullMarkerURL,
    width: 250,
  };
  const columns = {
    columns: [column, column],
  };
  var docDefinition = {
    content: [columns, columns, columns],
  };
  pdfMake.createPdf(docDefinition).open();
}

function handleFileInput(inputEvent) {
  const file = inputEvent.target.files[0];

  let reader = new FileReader();
  reader.onload = (event) => {
    innerImageURL = event.target.result;
    updateFullMarkerImage();
  };
  reader.readAsDataURL(file);
}

function handleDownloadFullImage() {
  if (innerImageURL === null) {
    alert("upload a file first");
    return;
  }
  createDownloadHyperlink()
}

function createDownloadHyperlink() {
  let domElement = window.document.createElement("a");
  domElement.href = fullMarkerURL;
  domElement.download = "marker.png";
  document.body.appendChild(domElement);
  domElement.click();
  document.body.removeChild(domElement);
}