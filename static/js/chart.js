'use strict';


//  // JS 
//  var chart = JSC.chart('chartDiv', { 
//   debug: true, 
//   type: 'calendar year solid', 
//   data: './resources/CarSales_2017.csv', 
//   defaultCultureName: 'es-MX', 
//   annotations: [ 
//     { 
//       position: 'top left', 
//       label_text: 
//         'Culture settings will format all labels.'
//     } 
//   ], 
//   legend_visible: false, 
//   defaultBox_boxVisible: false, 
//   toolbar_items: { 
//     culture: { 
//       type: 'select', 
//       position: 'top', 
//       label_text: 'Culture: %value', 
//       events_change: function(val) { 
//         setCulture(val); 
//       }, 
//       items: 
//         'en-US,es-MX,pl-PL,de-DE,fr-FR,ja-JP', 
//       value: 'es-MX'
//     } 
//   } 
// }); 
// function setCulture(val) { 
//   chart.options({ defaultCultureName: val }); 
// } 



// google.charts.load("current", {packages:["calendar"]});
// google.charts.setOnLoadCallback(drawChart);

// function drawChart() {
//  var dataTable = new google.visualization.DataTable();
//  dataTable.addColumn({ type: 'date', id: 'Date' });
//  dataTable.addColumn({ type: 'number', id: 'Won/Loss' });
//  dataTable.addRows([
//     [ new Date(2012, 3, 13), 37032 ],
//     [ new Date(2012, 3, 14), 38024 ],
//     [ new Date(2012, 3, 15), 38024 ],
//     [ new Date(2012, 3, 16), 38108 ],
//     [ new Date(2012, 3, 17), 38229 ],
//     // Many rows omitted for brevity.
//     [ new Date(2013, 9, 4), 38177 ],
//     [ new Date(2013, 9, 5), 38705 ],
//     [ new Date(2013, 9, 12), 38210 ],
//     [ new Date(2013, 9, 13), 38029 ],
//     [ new Date(2013, 9, 19), 38823 ],
//     [ new Date(2013, 9, 23), 38345 ],
//     [ new Date(2013, 9, 24), 38436 ],
//     [ new Date(2013, 9, 30), 38447 ]
//   ]);

//  var chart = new google.visualization.Calendar(document.getElementById('calendar_basic'));

//  var options = {
//    title: "Red Sox Attendance",
//    height: 350,
//  };

//  chart.draw(dataTable, options);
// }





// // JS 
// const chart; 
  
// JSC.fetch('./resources/temperatureComparison.csv') 
//   .then(function(response) { 
//     return response.text(); 
//   }) 
//   .then(function(text) { 
//     const data = JSC.csv2Json(text); 
//     chart = renderChart(makeSeries(data)); 
//   }); 
  
// function renderChart(series) { 
//   return JSC.chart('chartDiv', { 
//     type: 'calendar month solid', 
//     title_label: { 
//       text: 
//         'Air Temperature in Phoenix, AZ Сomparison of <icon name=material/action/timeline verticalAlign=middle color=#5c6bc0 size=20> <span color=#5c6bc0>1990</span> and <icon name=material/action/timeline color=#ec407a size=20> <span color=#ec407a>2018</span>', 
//       style_fontSize: 16 
//     }, 
//     defaultAxis: { 
//       defaultTick_line_visible: false, 
//       scale_interval: 1 
//     }, 
//     defaultSeries_shape_innerPadding: 0.017, 
//     yAxis_visible: false, 
//     toolbar_visible: false, 
//     legend: { 
//       position: 'right top', 
//       template: '%name', 
//       defaultEntry: { 
//         height: 30, 
//         width: 40, 
//         style_fontSize: '15px'
//       } 
//     }, 
//     calendar: { 
//       range: ['1/1/1990', '12/31/1990'], 
//       defaultEdgePoint: { 
//         mouseTracking: false, 
//         label_visible: false, 
//         color: 'white', 
//         outline_width: 0 
//       } 
//     }, 
//     defaultPoint: { 
//       outline_color: 'white', 
//       focusGlow_width: 0, 
//       margin: 0 
//     }, 
//     series: series 
//   }); 
// } 
  
// function makeSeries(data) { 
//   const series = JSC.nest() 
//     .key({ key: 'time', pattern: 'day' }) 
//     .pointRollup(function(key, val) { 
//       const tooltip = ''; 
//       const color = ''; 
//       if ( 
//         JSC.sum(val, 'temp_1990') < 
//         JSC.sum(val, 'temp_2018') 
//       ) { 
//         tooltip = 
//           'This day in 2018 was <b>warmer</b> than in 1990'; 
//         color = '#ec407a'; 
//       } else { 
//         tooltip = 
//           'This day in 2018 was <b>colder</b> than in 1990'; 
//         color = '#5c6bc0'; 
//       } 
//       return { 
//         date: new Date(key), 
//         attributes: { 
//           temp1990: 
//             '<chart width=90 height=68 align=center min=27 max=122 verticalAlign=top type=sparkline data=' + 
//             val 
//               .map(function(a) { 
//                 return a.temp_1990; 
//               }) 
//               .join(',') + 
//             ' color=#5c6bc0>', 
//           temp2018: 
//             '<chart width=90 height=68 align=center min=27 max=122 verticalAlign=top type=sparkline data=' + 
//             val 
//               .map(function(a) { 
//                 return a.temp_2018; 
//               }) 
//               .join(',') + 
//             ' color=#ec407a>', 
//           min1990: JSC.min(val, 'temp_1990'), 
//           max1990: JSC.max(val, 'temp_1990'), 
//           min2018: JSC.min(val, 'temp_2018'), 
//           max2018: JSC.max(val, 'temp_2018') 
//         }, 
//         color: [color, 0.1], 
//         states_hover_color: [color, 0.25], 
//         label_text: 
//           '<span style="align:left;font-size:13px;color:#9E9E9E"><b>%name</b></span><br><absolute>%temp1990%temp2018</absolute>', 
//         tooltip: 
//           '<b>{%date:date m}</b><br>Max/Min Temperature in 1990: <span color=#5c6bc0><b>%max1990°/%min1990°F</b></span><br>' + 
//           'Max/Min Temperature in 2018: <span color=#ec407a><b>%max2018°/%min2018°F</b></span><br>' + 
//           tooltip 
//       }; 
//     }) 
//     .series(data); 
//   return series; 
// } 




// const chart, 
//   chartConfig = { 
//     type: 'calendar month solid', 
//     calendar_calculation: 'average', 
//     legend: { 
//       visible: true, 
//       template: '%name', 
//       position: 'bottom', 
//       defaultEntry: { style_fontSize: 14 } 
//     }, 
//     palette: { 
//       colors: [ 
//         '#0000E3', 
//         '#0047FF', 
//         '#00ABFF', 
//         '#0FFFEF', 
//         '#43FFBB', 
//         '#73FF8B', 
//         '#A7FF57', 
//         '#FFEF00', 
//         '#FF8B00', 
//         '#FF5700', 
//         '#FF2300', 
//         '#ED0000', 
//         '#830000'
//       ], 
//       colorBar_axis_defaultTick_label_text: 
//         '{%value:n1}ºF'
//     }, 
//     title: { 
//       label_text: 'Temperature Jan-Apr 2018', 
//       position: 'center', 
//       style_fontSize: 16 
//     }, 
//     defaultTooltip_enabled: false, 
//     yAxis_visible: false, 
//     xAxis_line_visible: false, 
//     defaultSeries: { 
//       defaultPoint: { 
//         label: { 
//           text: 
//             '<b>{%date:date dd}</b><br><br><chart width=87 height=45 align=center verticalAlign=middle type=sparkline data=%subvalueList colors=white,none,none,green min=21.215 max=71.416>', 
//           autoHide: false
//         } 
//       } 
//     }, 
//     toolbar_visible: false
//   }; 
  
// loadData(makeChart); 

// function makeChart(data) { 
//     chartConfig.data = data; 
//     chart = JSC.chart('chartDiv', chartConfig); 
//   } 




// // Config
// const moodChart = new Chart(document.querySelector('#test-chart'), {
//     type: 'bubble',
//     data: {
//         labels: ['does', 'this', 'work'],
//         datasets: [
//             {data: [2, 4, 7]}
//         ]
//     },
//     options: {
//       responsive: true,
//       plugins: {
//         legend: {
//           position: 'top',
//         },
//         title: {
//           display: true,
//           text: 'Chart.js Bubble Chart'
//         }
//       }
//     },
//   });




// // Config
// const moodChart = new Chart(document.querySelector('#test-chart'), {
//     type: 'bubble',
//     data: data,
//     options: {
//       responsive: true,
//       plugins: {
//         legend: {
//           position: 'top',
//         },
//         title: {
//           display: true,
//           text: 'Chart.js Bubble Chart'
//         }
//       }
//     },
//   });


// // Setup  
// const DATA_COUNT = 7;
// const NUMBER_CFG = {count: DATA_COUNT, rmin: 5, rmax: 15, min: 0, max: 100};

// const labels = Utils.months({count: 7});
// const data = {
//   labels: labels,
//   datasets: [
//     {
//       label: 'Dataset 1',
//       data: Utils.bubbles(NUMBER_CFG),
//       borderColor: Utils.CHART_COLORS.red,
//       backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
//     },
//     {
//       label: 'Dataset 2',
//       data: Utils.bubbles(NUMBER_CFG),
//       borderColor: Utils.CHART_COLORS.orange,
//       backgroundColor: Utils.transparentize(Utils.CHART_COLORS.orange, 0.5),
//     }
//   ]
// };



// // Actions
// const actions = [
//     {
//       name: 'Randomize',
//       handler(chart) {
//         chart.data.datasets.forEach(dataset => {
//           dataset.data = Utils.bubbles({count: chart.data.labels.length, rmin: 5, rmax: 15, min: 0, max: 100});
//         });
//         chart.update();
//       }
//     },
//     {
//       name: 'Add Dataset',
//       handler(chart) {
//         const data = chart.data;
//         const dsColor = Utils.namedColor(chart.data.datasets.length);
//         const newDataset = {
//           label: 'Dataset ' + (data.datasets.length + 1),
//           backgroundColor: Utils.transparentize(dsColor, 0.5),
//           borderColor: dsColor,
//           data: Utils.bubbles({count: data.labels.length, rmin: 5, rmax: 15, min: 0, max: 100}),
//         };
//         chart.data.datasets.push(newDataset);
//         chart.update();
//       }
//     },
//     {
//       name: 'Add Data',
//       handler(chart) {
//         const data = chart.data;
//         if (data.datasets.length > 0) {
  
//           for (let index = 0; index < data.datasets.length; ++index) {
//             data.datasets[index].data.push(Utils.bubbles({count: 1, rmin: 5, rmax: 15, min: 0, max: 100})[0]);
//           }
  
//           chart.update();
//         }
//       }
//     },
//     {
//       name: 'Remove Dataset',
//       handler(chart) {
//         chart.data.datasets.pop();
//         chart.update();
//       }
//     },
//     {
//       name: 'Remove Data',
//       handler(chart) {
//         chart.data.labels.splice(-1, 1); // remove the label first
  
//         chart.data.datasets.forEach(dataset => {
//           dataset.data.pop();
//         });
  
//         chart.update();
//       }
//     }
//   ];   

