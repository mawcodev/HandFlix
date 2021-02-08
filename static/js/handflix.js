/*File: handflix.js
Description: This file contain the functions to control the videoplayer
Author: Diana Hernandez Soler
*/

const webcam = document.querySelector("aside.debug");
const media = document.getElementsByTagName("video")[0];
const output = document.querySelector("p.output");
let currentGesture = "";
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
  window.setInterval(getGesture, 500);
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
  }
}
