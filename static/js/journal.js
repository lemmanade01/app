'use strict';

const btn = document.querySelector('#show-journal-entries');

btn.addEventListener('click', (evt) => {
    evt.preventDefault();

    fetch('/journal-data.json')
    .then(response => response.json())
    .then(responseData => {
        console.log(responseData);
        console.log(Object.keys(responseData));

        const datesAndScale = [];
        let count = 1;

        for (const key of Object.keys(responseData)) {
           console.log(responseData[key]['scale']);
           console.log(responseData[key]['time_stamp']);
           
           // The month in all lowercase letters
           const mnth = responseData[key]['mnth'];
           // Make the first letter of each month capitalized
           const str1 = mnth.charAt(0);
           const str1Upper = str1.toUpperCase();
           const str2 = mnth.slice(1);
           // The month as a proper noun
           const upperMnth = str1Upper + str2;
           
           // Get the timestamp of the journal entry
           const timeStamp = responseData[key]['time_stamp'];
           console.log(timeStamp);
           // Slice the timestamp to extract the day
           const day = timeStamp.slice(5, 8);
           // Slice the timestamp to extract the year
           const year = timeStamp.slice(12, 16);

           // Get remaining journal data to display on user's page
           const scale = responseData[key]['scale'];
           const mood = responseData[key]['mood'];
           const g1 = responseData[key]['gratitude_1'];
           const g2 = responseData[key]['gratitude_2'];
           const g3 = responseData[key]['gratitude_3'];
           const reflection = responseData[key]['journal_input'];
           
           // Insert each journal entry with their corresponding data into the DOM
           const entries = document.querySelector('#display-entries-container').insertAdjacentHTML('beforeend', 
               `<div class="entry">
                    <h3>Journal ${count}</h3>
                    <p class="date">${upperMnth} ${day}, ${year}</p>
                    <p>Today you felt ${mood} and marked a ${scale}.</p>
                    <p>Gratitude List</p>
                    <ul>
                        <li>${g1}</li>
                        <li>${g2}</li>
                        <li>${g3}</li>
                    </ul>
                    <h5>Observations and Notes:</h5>
                    <p>${reflection}</p>
               </div><br>`
           );

           count += 1;
       }
    });
});