'use strict';

// // Deactivate the reamining mood buttons when one is selected
// // Store value of selected button into a constant

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
        console.log('The mood button has been clicked')
        // Disable that specific mood button
        // if (moodBtn.disabled == false){
        for (const mdBtn of moodBtns) {
            mdBtn.disabled = true;
        }
      
        
        // const timeStamps = new Date();
        // console.log(timeStamps);
        // const parsedDateTimes = Date.parse(timeStamps)
        // console.log(parsedDateTimes);


        console.log('The mood buttons have been disabled');

        // Get the value of that specific mood button
        const moodBtnValue = moodBtn.value;
        console.log(moodBtnValue);
        
        // separate the two values stored in its value
        const moodBtnValuesArr = moodBtnValue.split(' ');
        const moodValue = moodBtnValuesArr[0];
        selectedBtnValues.push(moodValue);
        console.log('mood: ', moodValue);
        const hexValue = moodBtnValuesArr[1];
        selectedBtnValues.push(hexValue);
        console.log('hex: ', hexValue);

        document.querySelector('.selected-mood').innerHTML = `I am feeling <strong>${moodValue}</strong>.`
    })
}

const journalSubmission = document.querySelector('#journal-submission');

journalSubmission.addEventListener('click', (evt) => {
    evt.preventDefault();
    
    const scale = document.querySelector('input[name="scale"]:checked').value;

    const mood = selectedBtnValues[0]
    const hexColor = selectedBtnValues[1]

    const gratitude1 = document.querySelector('#gratitude-1').value;

    const gratitude2 = document.querySelector('#gratitude-2').value;

    const gratitude3 = document.querySelector('#gratitude-3').value;

    const journal = document.querySelector('.journal-field').value;
    console.log('Journal Input:', journal);

    const journalValues = {
        scale: scale,
        mood: mood,
        color: hexColor,
        gratitude1: gratitude1,
        gratitude2: gratitude2,
        gratitude3: gratitude3,
        journal: journal
    };
    console.log(journalValues);

    // send a fetch request to the '/journal.json' route so that journal entry can be created on the back-end and stored in the database
    fetch('/journal.json', {
        method: 'POST',
        body: JSON.stringify(journalValues),
        headers: {
            'Content-Type': 'application/json'
        },
        // return the promised response in JSON
    })
    .then(response => response.json())
    .then(responseJson => {
            console.log('Success!: ', responseJson);
            // alert('Cheers! You have logged your journal entry. Keep up the self-reflection!');

            // window.location.href = '/journal-success';
    });    
});