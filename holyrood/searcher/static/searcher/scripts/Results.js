
function init(data, lastYearWithFullData) {
  
  console.log('JSON DATA:')
  console.log(data);

  var timeStepMonths = 12; //12mo for yearly output
  var updatingStartDate = moment().subtract(10, 'years'); // moment(`01-01-1999`);
  var finalEndDate = moment(`01-01-${lastYearWithFullData}`);
  var dateRanges = [];
  var isYear = (timeStepMonths === 12)
  while (finalEndDate > updatingStartDate ||
    (!isYear && updatingStartDate.format('M') === finalEndDate.format('M')) ||
    (isYear && updatingStartDate.format('Y') === finalEndDate.format('Y'))) {
    var startDate = moment(updatingStartDate);
    var endDate = moment(updatingStartDate);
    endDate.add(timeStepMonths,'month')
    dateRanges.push({
      start: startDate,
      end: endDate,
      quantity: 0
    })
    updatingStartDate = endDate.get();
  }

  for (var i = 0; i < data.length; i++) {
    var itemMonth = moment(data[i].fields.date);
    var range = dateRanges.find((dr) => itemMonth.isBetween(dr.start, dr.end))
    if (range) range.quantity++;
  }

  var labels = dateRanges.map((dr) => isYear ? dr.start.format('YY') : dr.start.format('YY-MM'))
  var series = dateRanges.map((dr) => dr.quantity)
  
  var chartData = {
    labels,
    series: [ series ]
  };

  var chartArgs = { axisY: { onlyInteger: true } };

  console.log('CHART DATA:')
  console.log(chartData);

  new Chartist.Line('.ct-chart', chartData, chartArgs);

}