
  $(document).ready(function () {

    $("#reg").on('click', function (event) {
        exportTableToCSV.apply(this, [$('#register'), 'register_records.csv']);
    });

    });
