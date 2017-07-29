import moment from 'moment';

export const getAverageMonthlyNutrition = async () => {
  const endYear = moment().year();
  const endMonth = moment().month();
  const endDay = moment().date();

  const startYear = moment().subtract(1, 'months').year();
  const startMonth = moment().subtract(1, 'months').month();
  const startDay = moment().subtract(1, 'months').date();

  const response = await fetch('http://localhost:5000/api/average/totals', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "start-year": startYear,
      "start-month": startMonth,
      "start-day": startDay,
      "end-year": endYear,
      "end-month": endMonth,
      "end-day": endDay,
    },
    credentials: 'same-origin'
  });
  const res = await response.json();
  return res;
}

export const getMonthlyEntries = async () => {
  const endYear = moment().year();
  const endMonth = moment().month();
  const endDay = moment().date();

  const startYear = moment().subtract(1, 'months').year();
  const startMonth = moment().subtract(1, 'months').month();
  const startDay = moment().subtract(1, 'months').date();

  const response = await fetch('http://localhost:5000/api/range/entries', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "start-year": startYear,
      "start-month": startMonth,
      "start-day": startDay,
      "end-year": endYear,
      "end-month": endMonth,
      "end-day": endDay,
    },
    credentials: 'same-origin'
  });
  const res = await response.json();
  return res;
}

export const fetchInitialData = async () => {
  const promises = [getMonthlyEntries(), getAverageMonthlyNutrition()];
  return Promise.all(promises)
}