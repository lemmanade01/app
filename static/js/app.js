'use strict';


// Get all buttons with the class 'heart-btn' as a NodeList
const heartBtns = document.querySelectorAll('.heart-btn');

// Convert buttons NodeList to an array
const heartBtnsArr = Array.prototype.slice.call(heartBtns);

// Loop through all of the queried meditation heart buttons
for (const heartBtn of heartBtnsArr) {
    
    // Add an event listener for each meditation heart button
    heartBtn.addEventListener('click', (evt) => {
        evt.preventDefault();
        console.log('The button has been clicked!');
       
        const heartBtnValue = heartBtn.value;
     
        // the element the event came from
        // const button = evt.target;
     
        // When a button has been clicked, check to see if its class value is 'btn-light'
        if (heartBtn.classList.contains('btn-light')) {
            heartBtn.classList.remove('btn-light');
            heartBtn.classList.add('btn-dark');

            // if yes, query the value of that specific button which is the meditation's id
            const favMeditation = {
                meditation_id: heartBtnValue
            }
            console.log(favMeditation);

            // send a fetch request to the '/favorite.json' route so that favorite can be created on the back-end and stored in the database
            fetch('/favorite.json', {
                method: 'POST',
                body: JSON.stringify(favMeditation),
                headers: {
                    'Content-Type': 'application/json'
                },
                // return the promised response in JSON
            })
                .then(response => response.json())
                .then(responseJson => {
                    console.log(responseJson);
                });
          // When a button has been clicked, check to see if its class value is 'btn-dark'
        } else if (heartBtn.classList.contains('btn-dark')) {
            heartBtn.classList.remove('btn-dark');
            heartBtn.classList.add('btn-light');
        
            // if yes, query the value of that specific button which is the meditation's id
            const favMeditation = {
                meditation_id: heartBtnValue
            }
            console.log(favMeditation);
            // send a fetch request to the '/remove-favorite.json' route so that favorite can be removed from the database
            fetch('/remove-favorite.json', {
                method: 'POST',
                body: JSON.stringify(favMeditation),
                headers: {
                    'Content-Type': 'application/json'
                },
                // return the promised response in JSON
            })
                .then(response => response.json())
                .then(responseJson => {
                    console.log(responseJson);
                });
        }
    });
}