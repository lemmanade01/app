'use strict';

// const quotePage= document.querySelector('.quote-page');

// quotePage.addEventListener('mouseover', (evt) => {
//         console.log('You are hovering!');
       
//         const audio = document.querySelector('.sea-preview');
//         audio.muted = false;
//         audio.play();
//         console.log('Sound has played');
//     })

// quotePage.addEventListener('mouseout', (evt) => {
//     console.log('You are hovering!');
    
//     const audio = document.querySelector('.sea-preview');
//     audio.play();
//     console.log('Sound has played');
// })
        

// Delay the appearance of the enter button
// Insert Enter button into DOM after 3 seconds
const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

const showEnterButton = async () => {
    await sleep(3000);
    const button = document.querySelector('#enter-button-container').insertAdjacentHTML('afterbegin', `<form action="/suggested-meditation"><button id="enter">Enter</div></form>`);
}

showEnterButton()