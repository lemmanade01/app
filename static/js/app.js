// Get all buttons with the class 'heart-btn' as a NodeList
const heartBtns = document.querySelectorAll('.heart-btn');

// Convert buttons NodeList to an array
const heartBtnsArr = Array.prototype.slice.call(heartBtns);

// Loop through all of the queried meditation heart buttons
for (const heartBtn of heartBtnsArr) {
    // Add an event listener for each meditation heart button
    heartBtn.addEventListener('click', (evt) => {
        evt.preventDefault();
        console.log(evt);
        const button = evt.target;
       
        console.log(button);
        console.log('The button has been clicked!');

        // When a button has been clicked, check to see if its class value is 'btn-light'
        if (button.className === 'btn-light') {
            button.classList.remove('.btn-light');
            button.classList.add('.btn-dark');

            // if yes, query the value of that specific button which is the meditation's id
            const favMeditation = {
                meditation_id: document.querySelector('.heart-btn').value
            }

            // send a fetch request to the '/favorite.json' route so a favorite can be created on the back-end and stored in the database
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
        } else if (heartBtn.className === 'btn-dark') {
            button.classList.remove('.btn-dark');
            button.classList.add('.btn-light');
        
            // if yes, query the value of that specific button which is the meditation's id
            const favMeditation = {
                meditation_id: document.querySelector('.heart-btn').value
            }

            // send a fetch request to the '/remove-favorite.json' route so a favorite can be removed from the database
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



// const searchInput = document.querySelector('#search-input').addEventListener('keyup', (evt) => {
//   const searchString = evt.target.value;
// })