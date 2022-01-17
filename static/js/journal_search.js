'use strict';

// Select the search-by-date button when clicked
const dateBtn = document.querySelector('#jrnl-search-submit').addEventListener('click', (evt) => {
    evt.preventDefault();
    console.log('Ive been clicked');

    // Get the user's selected date
    const date = document.querySelector('#jrnl-search-by-date').value;

    console.log(date);

    const jrnlDate = {
        date: date,
    };

    // Send a post fetch request to the server-side with the user's input value
    fetch('/journal-date-results.json', {   
        method: 'POST',
        body: JSON.stringify(jrnlDate),
        headers: {
            'Content-Type': 'application/json'
        },
    // Return the promised response in JSON and parse it to produce a javascript object
    })
        .then(response => response.json()) 
        .then(responseData => {
            console.log(responseData);

            // For loop over the object
            for (const key of Object.keys(responseData)) {
                console.log(key);

                // If the response data is not none, retrieve all the necessary values to display onto the page
                if (responseData[key] != "none") {
                    const mnth = responseData[key]['mnth'];
                    const timeStamp = responseData[key]['time_stamp'];
                    const dayOfWeek = timeStamp.slice(0,3);
                    const day = timeStamp.slice(5,7);
                    const yr = timeStamp.slice(12,16);
                    const mood = responseData[key]['mood'];
                    const scale = responseData[key]['scale'];
                    const gratitude1 = responseData[key]['gratitude_1'];
                    const gratitude2 = responseData[key]['gratitude_2'];
                    const gratitude3 = responseData[key]['gratitude_3'];
                    const jrnlInput = responseData[key]['journal_input'];

                    // Select this div container, manipulate the dom to display the results on the page without refreshing
                    document.querySelector('#display-entries-container').insertAdjacentHTML('beforeend', 
                    `<div class="row jrnl-search-results">
                        <div class="col-12 jrnl-search-container entry">
                            <div class="jrnl-search-txt-container">
                                <h5 class="jrnl-search-date class"> ${ dayOfWeek }, ${ mnth } ${ day } ${ yr }</h5>
                                <p class="jrnl-search-mood mood">Today you felt <strong>${ mood }</strong> and selected a <strong>${ scale }</strong> on the wellness scale</p>
                                <p class="jrnl-search-gratitude-list">Your Gratitude List:</p>
                                <p class="list">1. ${ gratitude1 }</p>
                                <p class="list">2. ${ gratitude2 }</p>
                                <p class="list">3. ${ gratitude3 }</p>
                                <h5 class="jrnl-search-notes-header">Observations and Notes:</h5>
                                <p class="jrnl-search-notes">${ jrnlInput }</p>
                            </div>
                        </div><br>
                    </div>`)
                  // If no journal entries exist, insert a statement 
                } else if (responseData[key] == {}) {
                    document.querySelector('#display-entries-container').insertAdjacentHTML('beforeend', `<p class="jrnl-search-no-entries">No journal entries match your date</p>`)
                } 
   
            }

        });             
});


// Select the view all journal entries button when clicked
const allJrnlsBtn = document.querySelector('#all-jrnls')
allJrnlsBtn.addEventListener('click', evt => {
    evt.preventDefault();
    console.log('the view all journal entries button has been clicked');

    // Send a fetch request to the server side
    fetch('/journal-data.json')
        .then(response => response.json())
        .then(responseData => {

            // For loop over the parsed data
            for (const key of Object.keys(responseData)) {

                // If a journal entry exists, retrieve all the necessary values to display onto the page
                if (responseData[key] != "no journal entries exist") {
                    const mnth = responseData[key]['mnth'];
                    const timeStamp = responseData[key]['time_stamp'];
                    const dayOfWeek = timeStamp.slice(0,3);
                    const day = timeStamp.slice(5,7);
                    const yr = timeStamp.slice(12,16);
                    const mood = responseData[key]['mood'];
                    const scale = responseData[key]['scale'];
                    const gratitude1 = responseData[key]['gratitude_1'];
                    const gratitude2 = responseData[key]['gratitude_2'];
                    const gratitude3 = responseData[key]['gratitude_3'];
                    const jrnlInput = responseData[key]['journal_input'];

                    // Select this div container, manipulate the dom to display the results on the page without refreshing
                    document.querySelector('#display-entries-container').insertAdjacentHTML('beforeend', 
                    `<div class="row jrnl-search-results">
                        <div class="col-12 jrnl-search-container entry">
                            <div class="jrnl-search-txt-container">
                                <h5 class="jrnl-search-date class"> ${ dayOfWeek }, ${ mnth } ${ day } ${ yr }</h5>
                                <p class="jrnl-search-mood mood">Today you felt <strong>${ mood }</strong> and selected a <strong>${ scale }</strong> on the wellness scale</p>
                                <p class="jrnl-search-gratitude-list">Your Gratitude List:</p>
                                <p class="list">1. ${ gratitude1 }</p>
                                <p class="list">2. ${ gratitude2 }</p>
                                <p class="list">3. ${ gratitude3 }</p>
                                <h5 class="jrnl-search-notes-header">Observations and Notes:</h5>
                                <p class="jrnl-search-notes">${ jrnlInput }</p>
                            </div>
                        </div><br>
                    </div>`)
                // If no journal entries exist, insert a statement 
                } else if (responseData[key] == {}) {
                    document.querySelector('#display-entries-container').insertAdjacentHTML('beforeend', `<p class="jrnl-search-no-entries">No journal entries exist yet</p>`)
        
                }
            }
        });
});