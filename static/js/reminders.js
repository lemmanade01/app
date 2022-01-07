'use strict';

// Schedule reminders
document.getElementById('submit-reminder').addEventListener('click', (evt) => {
    evt.preventDefault();
    console.log('Submit button has been clicked!');

    const reminderInput = document.querySelector('#reminder-description').value;

    const reminderType = document.querySelector('#reminder-type').value;

    const reminderTime = document.querySelector('#reminder-time').value;

    const reminder = {
        date: reminderTime,
        type: reminderType,
        description: reminderInput
    };
    console.log(reminder);
    // I want the events ordered chronologically
    // const displayReminder = document.querySelector('#display-reminders');

    // displayReminder.insertAdjacentHTML('beforeend', `<ul>Reminder: ${date}</ul><button>Delete Reminder</button>`);

    fetch('/schedule-reminder.json', {   
        method: 'POST',
        body: JSON.stringify(reminder),
        headers: {
            'Content-Type': 'application/json'
        },
    // return the promised response in JSON
})
    .then(response => response.json())
    .then(responseJson => {
        console.log('Success!: ', responseJson);
    });   
});