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

    fetch('/schedule-reminder.json', {   
        method: 'POST',
        body: JSON.stringify(reminder),
        headers: {
            'Content-Type': 'application/json'
        },
    // return the promised response in JSON
})
    .then(response => response.json())
    .then(responseData => {

        console.log('Success!: ', responseData);
        const id = responseData['ID']
        console.log(id);
        const type = responseData['type']
        const date = responseData['date']
        console.log(date);
        const month = date.slice(5, 7);
        console.log(month);
        let day = date.slice(8, 10);
        console.log(day);
        const yr = date.slice(0, 4);
        console.log(yr);

        let mth = ''
        if (month == '01') {
            mth = 'January'
        } else if (month == '02') {
            mth = 'February'
        } else if (month == '03') {
            mth = 'March'
        } else if (month == '04') {
            mth = 'April'
        } else if (month == '05') {
            mth = 'May'
        } else if (month == '06') {
            mth = 'June'
        } else if (month == '07') {
            mth = 'July'
        } else if (month == '08') {
            mth = 'August'
        } else if (month == '09') {
            mth = 'September'
        } else if (month == '10') {
            mth = 'October'
        } else if (month == '11') {
            mth = 'November'
        } else if (month == '12') {
            mth = 'December'
        }

        if (day.slice(0, 1) == '0') {
            day = day.slice(1);
        }
      
        const description = responseData['description']

        document.querySelector('.display-reminders').insertAdjacentHTML('afterbegin',
        `<div class="recently-added-reminder">
            <h3>Your Recently Added Reminders:</h3>
            <ul>
                <li>Reminder to: ${type} on ${mth} ${day}, ${yr}</li>
                    <p>Details: ${description}</p>
                    <button class="remove-reminder" value="${id}">Delete Reminder</button>
            </ul>
        </div>`)

    });   
});
    
    // I want the events ordered chronologically
    // const displayReminder = document.querySelector('#display-reminders');

    // displayReminder.insertAdjacentHTML('beforeend', `<ul>Reminder: ${date}</ul><button>Delete Reminder</button>`);





const btns = document.querySelectorAll('.remove-reminder');

    for (const btn of btns) {
        btn.addEventListener('click', (evt) => {

            console.log('Ive been clicked');
            const reminderId = document.querySelector('.remove-reminder').value;

            const reminderData = {
                reminder_id: reminderId
            }

            fetch('/remove-reminder.json', {
                method: 'POST',
                body: JSON.stringify(reminderData),
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(response2 => response2.json())
                .then(responseData2 => {
                    // btn.gparent(5).remove();
                    // btn.remove();
                    // btn.parentElement.parentElement.parentElement.parentElement.parentElement.remove();
                    btn.parentElement.remove();
                    console.log('Reminder removed');
                });
    });
}
