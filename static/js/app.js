'use strict';

// Spotify OAuth 2
// const client_id = process.env.SPOTIPY_CLIENT_ID;
// const redirect_uri = process.env.SPOTIFY_REDIRECT_URI;

// const app = express();

// app.get('/oauth-login', function(req, res) {

//   const state = generateRandomString(16);
//   const scope = 'user-read-private user-read-email';

//   res.redirect('https://accounts.spotify.com/authorize?' +
//     querystring.stringify({
//       response_type: 'code',
//       client_id: client_id,
//       scope: scope,
//       redirect_uri: redirect_uri,
//       state: state
//     }));
// });


// app.get('/callback', function(req, res) {

//     const code = req.query.code || null;
//     const state = req.query.state || null;
  
//     if (state === null) {
//       res.redirect('/#' +
//         querystring.stringify({
//           error: 'state_mismatch'
//         }));
//     } else {
//       const authOptions = {
//         url: 'https://accounts.spotify.com/api/token',
//         form: {
//           code: code,
//           redirect_uri: redirect_uri,
//           grant_type: 'authorization_code'
//         },
//         headers: {
//           'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
//         },
//         json: true
//       };
//     }
//   });




// const request = requirejs('request'); // "Request" library

// const client_id = process.env.SPOTIPY_CLIENT_ID; 
// const client_secret = process.env.SPOTIPY_CLIENT_SECRET;

// // your application requests authorization
// const authOptions = {
//   url: 'https://accounts.spotify.com/api/token',
//   headers: {
//     'Authorization': 'Basic ' + (new ArrayBuffer(client_id + ':' + client_secret).toString('base64'))
//   },
//   form: {
//     grant_type: 'client_credentials'
//   },
//   json: true
// };

// request.post(authOptions, function(error, response, body) {
//   if (!error && response.statusCode === 200) {

//     // use the access token to access the Spotify Web API
//     const token = body.access_token;
//     const options = {
//       url: 'https://api.spotify.com/v1/users/jmperezperez',
//       headers: {
//         'Authorization': 'Bearer ' + token
//       },
//       json: true
//     };
//     request.get(options, function(error, response, body) {
//       console.log(body);
//     });
//   }
// });




// fetch to get what things have been favorited in db and update DOM to reflect that

// User can favorite a meditation
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




// Deactivate the reamining mood buttons when one is selected
// Store value of selected button into a constant

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


        console.log('The mood button has been disabled');

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

journalSubmission.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const timeStamp = new Date();
    console.log(timeStamp);
    const parsedDateTime = Date.parse(timeStamp)
    console.log(parsedDateTime);

    const journalInput = document.querySelector('#journal-input').value;

    const gratitude1 = document.querySelector('#gratitude-1').value;

    const gratitude2 = document.querySelector('#gratitude-2').value;

    const gratitude3 = document.querySelector('#gratitude-3').value;

    const mood = selectedBtnValues[0]
    const hexColor = selectedBtnValues[1]
    // const allMoodBtns = document.querySelector('.all-mood-buttons');

    const journalValues = {
        mood: mood,
        color: hexColor,
        gratitude1: gratitude1,
        gratitude2: gratitude2,
        gratitude3: gratitude3,
        journal: journalInput,
        time: parsedDateTime
    };
    console.log(journalValues);

    console.log('Again: ', journalValues);
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
        });    
    });

