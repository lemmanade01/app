'use strict';

const btn = document.querySelector('#journal-search')
btn.addEventListener('click', evt => {
    evt.preventDefault();

    fetch('/journal-search-results.json')
        .then(response => response.json())
        .then(responseData => {
            
        })
})