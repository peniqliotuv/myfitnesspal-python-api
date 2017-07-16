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

