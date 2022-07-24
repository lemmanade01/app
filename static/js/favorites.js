'use strict';
// window.addEventListener('DOMContentLoaded', (event) => {
//     console.log('DOM fully loaded and parsed');

// Fetch to get what meditations have been favorited in db and update DOM to reflect that

// User can favorite a meditation
// Get all buttons with the class 'heart-btn' as a NodeList
const heartBtns = document.querySelectorAll('.heart-btn');

// Convert buttons NodeList to an array
// const heartBtnsArr = Array.prototype.slice.(callheartBtns);

heartBtns.forEach((btn) => {
    btn.addEventListener('click', (evt) => {
        if(evt == undefined)return;

        evt.preventDefault();
        // console.log('The button has been clicked!');
        // console.log(evt);
        
        // Target the element the event came from
        const heartBtnClicked = evt.target;
        // Retrieve that element's value
        const heartBtnValue = heartBtnClicked.value;
        // console.log(heartBtnClicked.value);
        // Get the class names of that element
        const heartBtnClasses = heartBtnClicked.classList;
        let url = '/add-favorite.json';
        
        // When a button has been clicked, check to see if its class value is 'btn-light'

            // if yes, query the value of that specific button which is the meditation's id
            if (heartBtnClasses.contains('btn-light')) {
                heartBtnClasses.remove('btn-light');
                heartBtnClasses.add('btn-dark');

                const favMeditation = {
                    meditation_id: heartBtnValue
                }
            
                // console.log(favMeditation);
                
                // Send a fetch request to the '/favorite.json' route so that favorite can be added to the database
                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify(favMeditation),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // Return the promised response in JSON
                }).then(response => response.json())
                    .then(responseJson => {
                        console.log("Success! Your favorite has been ADDED to the database.");
                    })         
                
            // Else, the clicked button has a class value of 'btn-dark'
            } else {

                url = '/remove-favorite.json';

                const favMeditation = {
                    meditation_id: heartBtnValue
                }

                // Send a fetch request to the '/remove-favorite.json' route so that favorite can be removed from the database
                fetch('/remove-favorite.json', {
                    method: 'POST',
                    body: JSON.stringify(favMeditation),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // Return the promised response in JSON
                }).then(response => response.json())
                    .then(responseJson => {
                        // console.log(responseJson);
                        console.log("Success! Your favorite has been REMOVED to the database.");
                        
                            });
                // If the clicked button's class contains favorite
                // Remove the entirety of its div contents
                if (heartBtnClasses.contains('favorite')) {
                    btn.parentElement.parentElement.remove();

                } else {
                // If the class value of the clicked button is 'btn-dark'
                // Change its value to 'btn-light'
                heartBtnClasses.remove('btn-dark');
                heartBtnClasses.add('btn-light');
                }
           
                    }
                });
            })


    
    
    // let last_button = null;
    // // Loop through all of the queried meditation heart buttons
    // for (const heartBtn of heartBtns) {
    //     // Add an event listener for each meditation heart button
    //     heartBtn.addEventListener('click', (evt) => {
    
    //         if(evt == undefined)return;
    
    //         evt.preventDefault();
    //         // console.log('The button has been clicked!');
    //         // console.log(evt);
           
    //         const heartBtnClicked = evt.target;
    //         const heartBtnValue = heartBtnClicked.value;
    //         // console.log(heartBtnClicked.value);
    //         const heartBtnClasses = heartBtnClicked.classList;
    //         let url = '/favorite.json';
    
    //         // The element the event came from
    //         // const button = evt.target;
         
    //         // When a button has been clicked, check to see if its class value is 'btn-light'
      
    //             // If yes, query the value of that specific button which is the meditation's id
    //             const favMeditation = {
    //                 meditation_id: heartBtnValue
    //             }
    //             // console.log(favMeditation);
    //             // Send a fetch request to the '/remove-favorite.json' route so that favorite can be removed from the database
                
    //             fetch(url, {
    //                 method: 'POST',
    //                 body: JSON.stringify(favMeditation),
    //                 headers: {
    //                     'Content-Type': 'application/json'
    //                 },
    //                 // Return the promised response in JSON
    //             }).then(response => response.json())
    //                 .then(responseJson => {
    
    //                     if (heartBtnClasses.contains('btn-light')) {
    //                         heartBtnClasses.remove('btn-light');
    //                         heartBtnClasses.add('btn-dark');
    //                         // if yes, query the value of that specific button which is the meditation's id
                    
    //                       // When a button has been clicked, check to see if its class value is 'btn-dark'
    //                     } else {
    //                         heartBtnClasses.remove('btn-dark');
    //                         heartBtnClasses.add('btn-light');
    //                         url = '/remove-favorite.json';
    
    //                         heartBtn.parentElement.parentElement.remove();
    
    //                         fetch('/remove-favorite.json', {
    //                             method: 'POST',
    //                             body: JSON.stringify(favMeditation),
    //                             headers: {
    //                                 'Content-Type': 'application/json'
    //                             },
    //                             // Return the promised response in JSON
    //                         }).then(response => response.json())
    //                             .then(responseJson => {
    //                                 // console.log(responseJson);
    //                             });
    //                     }
    //                 });
    //     });
    // }
