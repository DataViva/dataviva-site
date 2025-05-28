var data = {}

let yearsRange = {
    "rais": ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010",
        "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
    "secex": ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
        "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
}

$('#message').hide();
data.downloadLink = function () {
    dataSelection = []
    dataSelection.push($('#datasets').val());
    dataSelection.push($('select[name=year]').val());

    dataSelection = dataSelection.filter(function (n) { return n != "" && n !== null && n != "all" });
    return dataviva.s3_host + "/data-download/" + dataSelection[0] + "/" + lang + "/" + dataSelection.join("-") + '.csv.bz2';
}


$(document).ready(function () {
    $("#download").prop('disabled', true);
    $("#download").on('click', function () {
        window.open(data.downloadLink());
    });

    dataviva.requireAttrs(['datasets'], function () {
        $('#datasets').append($('<option value="rais" > ' + dataviva.dictionary["rais"] + '</option > '));
        $('#datasets').append($('<option value="secex">' + dataviva.dictionary["secex"] + '</option>'));
        $("#download").prop('disabled', true);

        $('#datasets').on('change', (e) => {
            $('#datasets #dataset-empty-option').remove();

            $('select[name=year]').empty().prop('disabled', false);
            $("#download").prop('disabled', false);

            yearsRange[e.currentTarget.value].forEach(function (year) {
                $('select[name=year]').append($('<option value="' + year + '">' + year + '</option>'));
            });

        });
    });
});
