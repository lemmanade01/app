// Display user's mood chart based on their journal entries
google.charts.load("current", {packages:["calendar"]});
google.charts.setOnLoadCallback(drawChart);

fetch('/journal-data.json')
    .then(response => response.json())
    .then(responseData => {
        console.log(responseData);
        const number = 3;
        console.log(Object.keys(responseData));

        const datesAndScale = [];
        
        for (const key of Object.keys(responseData)) {
           console.log(responseData[key]['scale']);
           console.log(responseData[key]['time_stamp']);

       }

    }
);


function drawChart() {
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'date', id: 'Date' });
    dataTable.addColumn({ type: 'number', id: 'Mood' });
    dataTable.addRows([
        // Many rows omitted for brevity.
        [ new Date(2022, 1, 06), 1 ],
        [ new Date(2022, 1, 07), 9 ],
        [ new Date(2022, 1, 08), 3 ],
        [ new Date(2022, 1, 11), 7 ],
        [ new Date(2022, 1, 20), 12 ],
        [ new Date(2022, 1, 26), 6 ],
        [ new Date(2022, 2, 3), 7 ],
        [ new Date(2022, 2, 7), 1 ],
        [ new Date(2022, 2, 14), 9 ],
        [ new Date(2022, 2, 15), 1 ],
        [ new Date(2022, 3, 16), 11 ],
        [ new Date(2022, 3, 17), 12 ]
      ]);

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