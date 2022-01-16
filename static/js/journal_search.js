'use strict';

const dateBtn = document.querySelector('#jrnl-search-submit').addEventListener('click', (evt) => {
    evt.preventDefault();
    console.log('Ive been clicked');

    const date = document.querySelector('#jrnl-search-by-date').value;

    console.log(date);

    const jrnlDate = {
        date: date,
    };


    fetch('/journal-date-results.json', {   
        method: 'POST',
        body: JSON.stringify(jrnlDate),
        headers: {
            'Content-Type': 'application/json'
        },
    // return the promised response in JSON
    })
        .then(response => response.json())
        .then(responseData => {
            console.log(responseData);

            for (const key of Object.keys(responseData)) {
                console.log(key);

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
                } else if (responseData[key] == {}) {
                    document.querySelector('#display-entries-container').insertAdjacentHTML('beforeend', `<p class="jrnl-search-no-entries">No journal entries match your date</p>`)
                } 
   
            }

        });             
});



const allJrnlsBtn = document.querySelector('#all-jrnls')
allJrnlsBtn.addEventListener('click', evt => {
    evt.preventDefault();
    console.log('the view all journal entries button has been clicked');

    fetch('/journal-data.json')
        .then(response => response.json())
        .then(responseData => {

            for (const key of Object.keys(responseData)) {

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
                }
            }
        });
});