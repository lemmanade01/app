'use strict';

const trackImgs = document.querySelectorAll('.track-img');

for (const trackImg of trackImgs) {
    trackImg.addEventListener('mouseover', (evt) => {
        // console.log('You are hovering!');
       
        const audio = document.querySelector('.audio-preview');
        audio.muted = false;
        audio.play();
        // console.log('Sound has played');
    })
        
}
    
for (const trackImg of trackImgs) {
    trackImg.addEventListener('mouseout', (evt) => {
        // console.log('You are no longer hovering');

        const audio = document.querySelector('.audio-preview');
        audio.muted = true;
        audio.pause();
        // audio.currentTime = 0;
    })
}