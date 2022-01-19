'use strict';

// Delay the appearance of the enter button
// Insert Enter button into DOM after 3 seconds
const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

const showEnterButton = async () => {
    await sleep(3000);
    const button = document.querySelector('#enter-button-container').insertAdjacentHTML('afterbegin', `<form action="/suggested-meditation"><button id="enter">Enter</div></form>`);
}

showEnterButton()