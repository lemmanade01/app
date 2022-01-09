'use strict';
// window.addEventListener('DOMContentLoaded', (event) => {
//     console.log('DOM fully loaded and parsed');


// Fetch to get what meditations have been favorited in db and update DOM to reflect that

// User can favorite a meditation
// Get all buttons with the class 'heart-btn' as a NodeList
const heartBtns = document.querySelectorAll('.heart-btn');

// Convert buttons NodeList to an array
// const heartBtnsArr = Array.prototype.slice.(callheartBtns);

let last_button = null;
// Loop through all of the queried meditation heart buttons
for (const heartBtn of heartBtns) {
    
    // Add an event listener for each meditation heart button
    heartBtn.addEventListener('click', (evt) => {

        if(evt == undefined)return;

        evt.preventDefault();
        console.log('The button has been clicked!');
        console.log(evt);
       
        const heartBtnClicked = evt.target;
        const heartBtnValue = heartBtnClicked.value;
        console.log(heartBtnClicked.value);
        const heartBtnClasses = heartBtnClicked.classList;
        let url = '/favorite.json';

        // The element ithe event came from
        // const button = evt.target;
     
        // When a button has been clicked, check to see if its class value is 'btn-light'
  
            // If yes, query the value of that specific button which is the meditation's id
            const favMeditation = {
                meditation_id: heartBtnValue
            }
            console.log(favMeditation);
            // Send a fetch request to the '/remove-favorite.json' route so that favorite can be removed from the database
            
            fetch(url, {
                method: 'POST',
                body: JSON.stringify(favMeditation),
                headers: {
                    'Content-Type': 'application/json'
                },
                // Return the promised response in JSON
            }).then(response => response.json())
                .then(responseJson => {

                    if (heartBtnClasses.contains('btn-light')) {
                        heartBtnClasses.remove('btn-light');
                        heartBtnClasses.add('btn-dark');
                        // if yes, query the value of that specific button which is the meditation's id
                
                      // When a button has been clicked, check to see if its class value is 'btn-dark'
                    } else {
                        heartBtnClasses.remove('btn-dark');
                        heartBtnClasses.add('btn-light');
                        url = '/remove-favorite.json';
                    }

                    console.log(responseJson);
                });
    });
}