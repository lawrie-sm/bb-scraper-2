// Switch into a spinner during search form submission
$(function() {
  $('#search-form').on('submit', function(e) {
      $("#loader-row").show();
      $("#content-row").hide();
  });
});

// Update chart and prevent form submission
$(function() {
  $('#results-chart').on('submit', function(e) {
      e.preventDefault();
      var formData = $('#results-chart').serializeArray();
      console.log(formData);
      setupChart(RECIEVED_DATA, END_YEAR, formData);
      return false;
  });
});

function setupChart(data, lastYearWithFullData, formData) {

  //console.log('JSON DATA:')
  //console.log(data);

  // Setup time span variables based on selection
  // 'last-year' is the default time-span
  var finalEndDate = moment(`01-01-${lastYearWithFullData}`);
  var timeStepMonths = 1;
  var updatingStartDate = moment(finalEndDate).subtract(1, 'years'); // moment(`01-01-1999`);

  // Setup default party data
  var parties = ['snp', 'lab', 'con', 'ld', 'green', 'others'];

  // Parse form data
    if (formData) {
    var timeSpan = formData[0].value;
    if (timeSpan != 'last-year') {
      if (timeSpan === 'last-3-years') {
        timeStepMonths = 3;
        updatingStartDate = moment(finalEndDate).subtract(3, 'years');
      } else if (timeSpan === 'last-10-years') {
        timeStepMonths = 12;
        updatingStartDate = moment(finalEndDate).subtract(10, 'years');
      } else if (timeSpan === 'all-time') {
        timeStepMonths = 12;
        updatingStartDate = moment(`01-01-1999`);
      }
    }
    parties = formData.map(function (d) {
      if (d.name === 'partyCheckboxes') return d.value;
    });
  }

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
      end: endDate
    })
    updatingStartDate = endDate.get();
  }
  for (var i = 0; i < data.length; i++) {
    var itemMonth = moment(data[i].fields.date);
    var range = dateRanges.find(function(dr) {
      return(itemMonth.isBetween(dr.start, dr.end));
      });
    if (range) {
      if (!range.quantity) range.quantity = 0;
      range.quantity++;
    }
  }

  var labels = dateRanges.map(function(dr) {
    return(isYear ? dr.start.format('YY') : dr.start.format('YY-MM'))
  });

  if (labels.length > 0) {
    var series = dateRanges.map(function (dr) {
      return(dr.quantity)
    });
    var chartData = {
      labels,
      series: [ series ]
    };
    var chartArgs = { axisY: { onlyInteger: true } };
    new Chartist.Line('.ct-chart', chartData, chartArgs);
    $('.ct-chart').show();
    $('#no-data-warning').hide();
    //console.log('CHART DATA:')
    //console.log(chartData);
  } else {
    $('.ct-chart').hide();
    $('#no-data-warning').show();
  }
}