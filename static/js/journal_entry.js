'use strict';

// Query all mood buttons
const moodBtns = document.querySelectorAll('.mood-button');

// Convert buttons NodeList to an array
const moodBtnsArr = Array.prototype.slice.call(moodBtns);

const selectedBtnValues = [];

// Add an event listener for each mood button
for (const moodBtn of moodBtnsArr) {
    // If a mood button is clicked
    moodBtn.addEventListener('click', (evt) => {
        evt.preventDefault();
        // console.log('The mood button has been clicked')
        // Disable all mood buttons when one is selected
        for (const mdBtn of moodBtns) {
            mdBtn.disabled = true;
        }

        // console.log('The mood buttons have been disabled');

        // Get the value of that specific mood button
        const moodBtnValue = moodBtn.value;
        // console.log(moodBtnValue);
        
        // Separate the two values stored in its value
        const moodBtnValuesArr = moodBtnValue.split(' ');
        const moodValue = moodBtnValuesArr[0];
        selectedBtnValues.push(moodValue);
        // console.log('mood: ', moodValue);
        const hexValue = moodBtnValuesArr[1];
        selectedBtnValues.push(hexValue);
        // console.log('hex: ', hexValue);

        document.querySelector('.selected-mood').innerHTML = `I am feeling <strong>${moodValue}</strong>.`
    })
}

const journalSubmission = document.querySelector('#journal-submission');

journalSubmission.addEventListener('click', (evt) => {
    evt.preventDefault();

    fetch('journal-check.json')
        .then(response => response.json())
        .then(responseData => {
            // console.log(responseData);
            const count = responseData['count'];
            // THIS COUNT IS INCORRECT! FIX IN CRUD.PY AND CORRECT ON SERVER SIDE
            if (count >= 1) {
                // FLASH MESSAGE TELLING USER THEY'VE ALREADY SUBMITTED THEIR JOURNAL ENTRY FOR THE DAY
                // const flashMessage = () => {

                // }
                // flash("You have already submitted your journal entry for today.")
                window.location.replace("/profile");
            } else {
                const scale = document.querySelector('input[name="scale"]:checked').value;

                const mood = selectedBtnValues[0]
                const hexColor = selectedBtnValues[1]
            
                const gratitude1 = document.querySelector('#gratitude-1').value;
            
                const gratitude2 = document.querySelector('#gratitude-2').value;
            
                const gratitude3 = document.querySelector('#gratitude-3').value;
            
                const journal = document.querySelector('.journal-field').value;
                // console.log('Journal Input:', journal);
            
                const journalValues = {
                    scale: scale,
                    mood: mood,
                    color: hexColor,
                    gratitude1: gratitude1,
                    gratitude2: gratitude2,
                    gratitude3: gratitude3,
                    journal: journal
                };
                // console.log(journalValues);
            
                // Send a fetch request to the '/journal.json' route so that journal entry can be created on the back-end and stored in the database
                fetch('/journal.json', {
                    method: 'POST',
                    body: JSON.stringify(journalValues),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // Return the promised response in JSON
                })
                .then(response => response.json())
                .then(responseJson => {
                        // console.log('Success!: ', responseJson);
                        // alert('Cheers! You have logged your journal entry. Keep up the self-reflection!');

                        // FLASH MESSAGE TELLING USER SUCCESS! THEY'VE SUBMITTED THEIR JOURNAL ENTRY FOR THE DAY
                        window.location.replace("/journal-success");
                });    
            }
        })
});