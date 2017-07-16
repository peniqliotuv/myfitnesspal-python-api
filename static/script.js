function submit() {
  var request = new XMLHttpRequest();
  request.open('POST', '/api/login', true);
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  var data = {
    "username": document.getElementById('username').value,
    "password": document.getElementById('password').value
  };
  request.send(JSON.stringify(data));
}

function getDataByDate() {
  var date = document.getElementById('date').value;
  date = date.split('/');
  var month = date[0];
  var day = date[1];
  var year = date[2];
  fetch('/api/day/totals', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
      "year": year,
      "month": month,
      "day": day
    },
    credentials: 'same-origin'
  }).then(function(data){
    return data.json();
  }).then(function(json) {
    console.log(json)
  });
  
}

function getMealsByDate() {
  var date = document.getElementById('date').value;
  date = date.split('/');
  var month = date[0];
  var day = date[1];
  var year = date[2];

  fetch('/api/day/meals', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
      "year": year,
      "month": month,
      "day": day
    },
    credentials: 'same-origin'
  }).then(function(data){
    return data.json();
  }).then(function(json) {
    console.log(json)
  });
}

function getWaterByDate() {
  var date = document.getElementById('date').value;
    date = date.split('/');
    var month = date[0];
    var day = date[1];
    var year = date[2];

    fetch('/api/day/water', {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "year": year,
        "month": month,
        "day": day
      },
      credentials: 'same-origin'
    }).then(function(data){
      return data.json();
    }).then(function(json) {
      console.log(json)
    });
}

function getEntriesByDate() {
  var date = document.getElementById('date').value;
    date = date.split('/');
    var month = date[0];
    var day = date[1];
    var year = date[2];

    fetch('/api/day/entries', {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "year": year,
        "month": month,
        "day": day
      },
      credentials: 'same-origin'
    }).then(function(data){
      return data.json();
    }).then(function(json) {
      console.log(json)
    });
}



function getRange() {
  console.log('clicked')
  var start = document.getElementById('start').value;
  var end = document.getElementById('end').value;

  start = start.split('/');
  var startMonth = start[0];
  var startDay = start[1];
  var startYear = start[2];

  end = end.split('/');
  var endMonth = end[0];
  var endDay = end[1];
  var endYear = end[2];


  fetch('/api/range/totals', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
      "start-year": startYear,
      "start-month": startMonth,
      "start-day": startDay,
      "end-year": endYear,
      "end-month": endMonth,
      "end-day": endDay,
    },
    credentials: 'same-origin'
  }).then(function(data){
    return data.json();
  }).then(function(json) {
    console.log(json)
  });
}