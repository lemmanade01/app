'use strict';

const trackImg = document.querySelector('#track-img');
trackImg.addEventListener("mouseover", (evt) => {
    console.log('You are hovering!');
   
    const audio = document.querySelector('#audio-preview');
    audio.muted = false;
    audio.play();
    console.log('Sound has played');
})

trackImg.addEventListener("mouseout", (evt) => {
    const audio = document.querySelector('#audio-preview');
    audio.muted = true;
    audio.stop();
    // audio.currentTime = 0;
})