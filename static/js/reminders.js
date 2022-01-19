'use strict';

// Function that removes reminders by reminder id when 'Delete Reminder' button is clicked
const removeReminder = () => {
    const btns = document.querySelectorAll('.remove-reminder');

    for (const btn of btns) {
        btn.addEventListener('click', (evt) => {
            // console.log('Ive been clicked');
            const reminderId = document.querySelector('.remove-reminder').value;
            // console.log(reminderId);

            const reminderData = {
                reminder_id: reminderId
            }
            // console.log(reminderData);

            fetch('/remove-reminder.json', {
                method: 'POST',
                body: JSON.stringify(reminderData),
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(response2 => response2.json())
                .then(responseData2 => {
                    // console.log('This reminder has been removed from the db');

                    // Remove the entire container for the reminder
                    btn.parentElement.parentElement.parentElement.parentElement.parentElement.remove();
                    // console.log('Reminder removed');

                    // Does a reminder from the database exist
                    const exist = !!document.querySelector('.reminder');
                    // console.log('does this element exist?  ', exist);

                    // If no, remove the header that states "Your Reminders:"
                    if (exist == false) {
                        document.getElementById('#reminders-header').remove();
                    }
                });
    });
    }
   
}

// Schedule reminders
document.querySelector('#reminders-submit').addEventListener('click', (evt) => {
    evt.preventDefault();
    // console.log('Submit button has been clicked!');

    const reminderInput = document.querySelector('#reminder-description').value;

    const reminderType = document.querySelector('#reminder-type').value;

    const reminderTime = document.querySelector('#reminder-time').value;
    const yr = reminderTime.slice(0,4);
    const mnth = reminderTime.slice(5,7);
    const day = reminderTime.slice(8,10);
    const date = yr + mnth + day;
    const scheduledDateInt = parseInt(date);
    // console.log('scheduled date:',scheduledDateInt);

    const today = new Date();
    let todayStr = today.toString();
    const yr2 = todayStr.slice(11,15);
    const mnth2 = todayStr.slice(4,7);
    const day2 = todayStr.slice(8,10);

    let month2 = '';
    if (mnth2 == 'Jan') {
        month2 = '01';
      } else if (mnth2 == 'Feb') {
        month2 = '02';
      } else if (mnth2 == 'Mar') {
        month2 = '03';
      } else if (mnth2 == 'Apr') {
        month2 = '04';
      } else if (mnth2 == 'May') {
        month2 = '05';
      } else if (mnth2 == 'Jun') {
        month2 = '06';
      } else if (mnth2 == 'Jul') {
        month2 = '07';
      } else if (mnth2 == 'Aug') {
        month2 = '08';
      } else if (mnth2 == 'Sep') {
        month2 = '09';
      } else if (mnth2 == 'Oct') {
        month2 = '10';
      } else if (mnth2 == 'Nov') {
        month2 = '11';
      } else if (mnth2 == 'Dec') {
        month2 = '12';
      } 

    const date2 = yr2 + month2 + day2;
    const todayDateInt = parseInt(date2);
    // console.log('today date:',todayDateInt);
   
    // console.log('Scheduled Date:', scheduledDateInt, '--> Today Date:', todayDateInt);

    if (scheduledDateInt >= todayDateInt) {
        const reminder = {
            date: reminderTime,
            type: reminderType,
            description: reminderInput
        };
    
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
        
                // console.log('Success!: ', responseData);
                const id = responseData['ID']
                // console.log(id);
                const type = responseData['type']
                const date = responseData['date']
                // console.log(date);
                const month = date.slice(5, 7);
                // console.log(month);
                let day = date.slice(8, 10);
                // console.log(day);
                const yr = date.slice(0, 4);
                // console.log(yr);
        
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
        
                const exist = !!document.querySelector('.no-reminders');
                // console.log('does this element exist?  ', exist);
                // console.log('length', description.length);
                
                if (exist == true) {
                    document.querySelector('.no-reminders').remove();
                }
                const add = document.querySelector('.recently-added-reminders');

                if (description.length > 0) {
                document.querySelector('.recently-added-reminders').insertAdjacentHTML('afterbegin',
                `<div class="recently-added-reminder reminders-scheduler-container">
                <h3 class="reminders-header">Your Recently Added Reminders:</h3>
                <div class="display-reminders">
                    <div class="reminder-info"> ${mth} ${day}, ${yr}</div>
                    <span class="italics">Reminder to:</span> <span class="reminder-info"> ${type}</span>
                        <div><span class="italics">Details:</span><span class="reminder-info"> ${description}</span></div>
                        <button class="remove-reminder" value="${id}">Delete Reminder</button>
                </div>
                </div>`)
        
                removeReminder();  
                } else {
                    document.querySelector('.recently-added-reminders').insertAdjacentHTML('afterbegin',
                    `<div class="recently-added-reminder reminders-scheduler-container">
                    <h3 class="reminders-header">Your Recently Added Reminders:</h3>
                    <div class="display-reminders">
                        <div class="reminder-info"> ${mth} ${day}, ${yr}</div>
                        <span class="italics">Reminder to:</span> <span class="reminder-info"> ${type}</span>
                            <div><span class="italics">Details:</span><span class="italics"> None</span></div>
                            <button class="remove-reminder" value="${id}">Delete Reminder</button>
                    </div>
                </div>`)
        
                removeReminder(); 
                }    
            });  
    } else {
            const msg = document.querySelector('.missing-field');
            msg.insertAdjacentHTML('afterbegin', `<span id="old-date">You must select a current or future date.</span>`);

            const timer = setTimeout( function() {
                msg.remove();
            }, 5000);
    }  
});
    
removeReminder();