const webcam = document.querySelector("aside.debug");
const media = document.querySelector("body>main>video");
const output = document.querySelector("p.output");
let currentGesture = "nothing";
let change = false;

(function () {
  getGesture = () => {
    fetch("./gesture")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        change = currentGesture !== data.gesture ? true : false;
        currentGesture = data.gesture;
      });

    output.innerHTML = `Gesture detected: ${currentGesture}`;
    if (change) videoController(currentGesture);
  };
  window.setInterval(getGesture, 5000);
})();

function videoController(current) {
  switch (current) {
    case "STOP":
      media.pause();
      media.currentTime = 0;
      break;
    case "PAUSE":
      media.pause();
      break;
    case "PLAY":
      media.play();
    default:
      output.innerHTML = `Gesture detected: NONE`;
  }
}
