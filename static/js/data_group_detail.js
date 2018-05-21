

  $(document).ready(function () {
    var table = $('#docs').DataTable({
      "serverSide": false,
      "paging": false,
      "searching": false,
      "ordering": true,
      "dom": 't'
    // "lengthMenu": [ 10, 25, 50, 75, 100 ], // change number of records shown
    // "columnDefs": [
    //     {
    //         "targets": [1,2,3,4],
    //         "orderable": false
    //     },
    // ],
    });

    var dg_name = document.getElementById("dg_name").value;
      // This must be a hyperlink
    $("#rr").on('click', function (event) {
        exportTableToCSV.apply(this, [$('#registered'), dg_name + '_registered_records.csv']);
    });

    $("#xx").on('click', function (event) {
        exportTableToCSV.apply(this, [$('#extract'), dg_name + '_extract_template.csv']);
    });

    // make submit button active when file selected
    $('input:file').change(
        function(){
            if ($(this).val()) {
                $('input:submit').attr('disabled',false);
            } else {
                $('input:submit').attr('disabled',true);
            }
        }
        );
    });
