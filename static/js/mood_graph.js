
// Make an AJAX call to server side to get all of user's journal data 
// to display their journal mood chart
fetch('/journal-data.json')
    .then(response => response.json())
    .then(responseData => {
          console.log(responseData);
          
          console.log(responseData['Response']);
          // const number = 3;
          console.log(Object.keys(responseData));
  
          // Display user's mood chart based on their journal entries
          google.charts.load("current", {packages:["calendar"]});
          google.charts.setOnLoadCallback(drawChart);
  
          function drawChart() {
            var dataTable = new google.visualization.DataTable();
            dataTable.addColumn({ type: 'date', id: 'Date' });
            dataTable.addColumn({ type: 'number', id: 'Mood' });
            
            let rows = [];
            
            for (const key of Object.keys(responseData)) {
              console.log(responseData[key]['scale']);
              console.log(responseData[key]['time_stamp']);
  
              const scale = responseData[key]['scale'];
              const scaleInt = parseInt(scale);
              console.log('Integer: ', scaleInt);
              // const scaleNum = Number(scale);
              // console.log('Number: ', scaleNum);
  
              const timeStamp = responseData[key]['time_stamp'];
              const mnth = timeStamp.slice(8, 11);
              console.log('mnth: ', mnth);
          
              const day = timeStamp.slice(5, 7);
              // console.log(day);
  
              const dayInt = parseInt(day);
              console.log('dayInt: ', dayInt);
  
              const year = timeStamp.slice(12, 16);
              // console.log(year);
              const yearInt = parseInt(year);
              console.log('yearInt: ', yearInt);
  
              let monthInt = 0;
  
              // new Date method starts the calendar year (January) with 0
              if (mnth == 'Jan') {
                monthInt = 0;
              } else if (mnth == 'Feb') {
                monthInt = 1;
              } else if (mnth == 'Mar') {
                monthInt = 2;
              } else if (mnth == 'Apr') {
                monthInt = 3;
              } else if (mnth == 'May') {
                monthInt = 4;
              } else if (mnth == 'Jun') {
                monthInt = 5;
              } else if (mnth == 'Jul') {
                monthInt = 6;
              } else if (mnth == 'Aug') {
                monthInt = 7;
              } else if (mnth == 'Sep') {
                monthInt = 8;
              } else if (mnth == 'Oct') {
                monthInt = 9;
              } else if (mnth == 'Nov') {
                monthInt = 10;
              } else if (mnth == 'Dec') {
                monthInt = 11;
              } 
              console.log('monthInt: ', monthInt);
              console.log('*************');
              // let a = `Test: [(${yearInt}, ${monthInt}, ${dayInt}), ${scaleInt} ]` 
              // let a = `${yearInt}` + `${monthInt}` + `${dayInt}` + `${scaleInt}` 
              // console.log(a);
              let dateForRow = new Date(`${yearInt}`, `${monthInt}`, `${dayInt}`)
              let scaleForRow = scaleInt;
  
              let row = [ dateForRow, scaleForRow ]
              console.log('Row: ', row);
              rows.push(row);
            }
  
            console.log('All rows: ', rows);
            
            dataTable.addRows(rows);
  
            var chart = new google.visualization.Calendar(document.getElementById('calendar_basic'));
  
            var options = {
              //title: "Mood Chart",
              height: 350,
              noDataPattern: {
              backgroundColor: '#fff8ee',
              //color: '#fff7ff'
              },
              calendar: { 
                cellSize: 17,
                focusedCellColor: {
                  stroke: '#5ee090',
                  strokeOpacity: 1,
                  strokeWidth: 1,
              },
                monthLabel : {
                  fontName: 'Trebuchet MS',
                  fontSize: 12,
                  color: '#7e2423',
                  bold: true
                },
                monthOutlineColor: {
                  stroke: '#ffc067',
                  strokeOpacity: 0.8,
                  strokeWidth: 2
                },
                unusedMonthOutlineColor: {
                  stroke: '#ffe1b7',
                  strokeOpacity: 0.8,
                  strokeWidth: 1
                },
                underMonthSpace: 7,
                underYearSpace: 10,
                yearLabel: {
                  fontName: 'Trebuchet MS',
                  fontSize: 40,
                  color: '#ffc067',
                  //color: '#ffb672',
                  bold: true,
                  //italic: true,
              },
                dayOfWeekLabel: {
                  fontName: 'Trebuchet MS',
                  fontSize: 12,
                  color: '#7e2423',
                  //color: '#acc0f3',
                  bold: true,
                  italic: false,
                },
                dayOfWeekRightSpace: 10,
                daysOfWeek: 'MTWTFSS',
              },
                colorAxis: {  
                  colors: ['#f36144', '#fad9fb']
                  //colors: ['#e3ff73', '#e27c39']
              }
            };
  
            chart.draw(dataTable, options);
          }
        }     
    })