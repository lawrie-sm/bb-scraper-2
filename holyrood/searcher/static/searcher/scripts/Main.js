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
      setupChart(RECIEVED_DATA, END_YEAR, formData);
      return false;
  });
});


// Main chart setup function
function setupChart(data, lastYearWithFullData, formData) {

  // Setup time span variables & defaults based on selection
  // 'last-year' is the default time-span
  var finalEndDate = moment(`01-01-${lastYearWithFullData}`);
  var timeStepMonths = 1;
  var updatingStartDate = moment(finalEndDate).subtract(1, 'years'); // moment(`01-01-1999`);

  // Set default type
  var type = 'all-types';

  // Setup default party data and 'parties' dict
  var DEFAULT_PARTIES = ['tot', 'snp', 'lab', 'con', 'ld', 'grn', 'oth'];
  var parties = { 'tot': 'y'}

  // Deal with inputs from the update form, if any
  if (formData) {
    var timeSpan = formData.find(function(v) {
      if (v.name === 'date-range') return v;
    }); 
    timeSpan = timeSpan.value;
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
    
    // Set type based on form
    type = formData.find(function(v) {
      if (v.name === 'type') return v;
    }); 
    type = type.value;

    // Build party dict from formData
    parties = {};
    for (var i = 0; i < formData.length; i++) {
      if (DEFAULT_PARTIES.includes(formData[i].name)) {
        parties[formData[i].name] = formData[i].value;
      }
    }
  }
  var partyList = Object.keys(parties);

  // Create date range objects
  var dateRanges = [];
  var isYear = (timeStepMonths === 12)
  while (finalEndDate > updatingStartDate ||
    (!isYear && updatingStartDate.format('M') === finalEndDate.format('M')) ||
    (isYear && updatingStartDate.format('Y') === finalEndDate.format('Y'))) {
    var startDate = moment(updatingStartDate);
    var endDate = moment(updatingStartDate);
    endDate.add(timeStepMonths,'month')
    var newRange = {
      start: startDate,
      end: endDate
    };
    for (var i = 0; i < partyList.length; i++) {
      newRange[partyList[i]] = 0;
    }
    dateRanges.push(newRange)
    updatingStartDate = endDate.get();
  }
  // Iterate through data and add quantities to each range object
  for (var i = 0; i < data.length; i++) {
    var itemMonth = moment(data[i].fields.date);
    var range = dateRanges.find(function(dr) {
      return(itemMonth.isBetween(dr.start, dr.end));
      });
    if (range) {
      pty = getPartyFromSPName(data[i].fields.party);
      if (range[pty] != undefined) range[pty]++;
      if (range['tot'] != undefined) range['tot']++;
    }
  }

  var labels = dateRanges.map(function(dr) {
    return(isYear ? dr.start.format('YY') : dr.start.format('YY-MM'))
  });

  var series = [];
  for (var i = 0; i < partyList.length; i++) {
    var newSeries = {
      className: `ct-${partyList[i]}`,
      data: [],
    }
    newSeries.data = dateRanges.map(function (dr) {
      return(dr[partyList[i]])
    })
    series[i] = newSeries;
  }
  if (labels.length > 0 && series.length > 0) {
    var chartData = {
      labels,
      series,
    };

    var chartArgs = { axisY: { onlyInteger: true } };
    new Chartist.Line('.ct-chart', chartData, chartArgs);
    $('.ct-chart').show();
    $('#no-data-warning').hide();
  } else {
    $('.ct-chart').hide();
    $('#no-data-warning').show();
  }
}

function getPartyFromSPName(SPName) {
  if (SPName === 'Scottish National Party') return 'snp';
  if (SPName === 'Scottish Labour') return 'lab';
  if (SPName === 'Scottish Conservative and Unionist Party') return 'con';
  if (SPName === 'Scottish Liberal Democrats') return 'ld';
  if (SPName === 'Scottish Green Party') return 'grn';
  return 'oth';
}