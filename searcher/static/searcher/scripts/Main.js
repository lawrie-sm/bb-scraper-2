$(function() {

  // Switch into a spinner during search form submission
  $('#search-form').on('submit', function(e) {
      $("#loader-row").show();
      $("#content-row").hide();
  });


  // Update chart and prevent form submission
  $('#results-chart').on('submit', function(e) {
      e.preventDefault();
      var formData = $('#results-chart').serializeArray();
      setupChart(RECIEVED_DATA, END_YEAR, formData);
      return false;
  });

  // Make the chart update form refresh on changes
  $('#results-chart').find('input').change(function(e) {
    $(this).closest('form').submit();
  });
});

// Main chart setup function
function setupChart(data, lastYearWithFullData, formData) {

  // Setup time span variables & defaults based on selection
  var finalEndDate = moment(`01-01-${lastYearWithFullData}`);
  var timeStepMonths = 12;
  var updatingStartDate = moment(`01-01-1999`);

  // Set default type
  var selectedType = 'all-types';

  // Setup default party data and 'parties' dict
  var DEFAULT_PARTIES = ['tot', 'snp', 'lab', 'con', 'ld', 'grn', 'oth'];
  var parties = {
    'snp': 'y',
    'lab': 'y',
    'con': 'y',
    'ld': 'y',
    'grn': 'y',
    'oth': 'y',
  }

  // Deal with inputs from the update form, if any
  if (formData) {
    var timeSpan = formData.find(function(v) {
      if (v.name === 'date-range') return v;
    }); 
    timeSpan = timeSpan.value;
    if (timeSpan === 'last-year') {
      timeStepMonths = 1;
      updatingStartDate = moment(finalEndDate).subtract(1, 'years');
    } else if (timeSpan === 'last-5-years') {
      timeStepMonths = 4;
      updatingStartDate = moment(finalEndDate).subtract(5, 'years');
    } else if (timeSpan === 'last-10-years') {
      timeStepMonths = 12;
      updatingStartDate = moment(finalEndDate).subtract(10, 'years');
    } else if (timeSpan === 'all-time') {
      timeStepMonths = 12;
      updatingStartDate = moment(`01-01-1999`);
    }

    // Set type based on form
    // selectedType = formData.find(function(v) {
    //   if (v.name === 'type') return v;
    // }); 
    // selectedType = selectedType.value;

    // Build party dict from formData
    parties = {};
    for (var i = 0; i < formData.length; i++) {
      if (DEFAULT_PARTIES.includes(formData[i].name)) {
        parties[formData[i].name] = formData[i].value;
      }
    }
  }
  var partyList = Object.keys(parties);

  var finalTotal = 0

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
    if (range && typeIsIncluded(data[i].model, selectedType)) {
      pty = getPartyFromSPName(data[i].fields.party);
      if (range[pty] != undefined) range[pty]++;
      if (range['tot'] != undefined) range['tot']++;
      finalTotal++;
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
  var chartData = {
    labels,
    series,
  };

  var chartArgs = { axisY: { onlyInteger: true } };
  new Chartist.Line('.ct-chart', chartData, chartArgs);
  $('.ct-chart').show();

  $('#final-total').empty().append(`Found ${finalTotal} instance(s)`);
}

function getPartyFromSPName(SPName) {
  if (SPName === 'Scottish National Party') return 'snp';
  if (SPName === 'Scottish Labour') return 'lab';
  if (SPName === 'Scottish Conservative and Unionist Party') return 'con';
  if (SPName === 'Scottish Liberal Democrats') return 'ld';
  if (SPName === 'Scottish Green Party') return 'grn';
  return 'oth';
}

function typeIsIncluded(model, selectedType) {
if (selectedType === 'all-types') return true;
if (model === 'searcher.motion' && selectedType === 'motions') return true;
if (model === 'searcher.question' && selectedType === 'questions') return true;
if (model === 'searcher.contribution' && selectedType === 'contribs') return true;
return false;
}