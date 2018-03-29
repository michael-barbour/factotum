

  $(document).ready(function () {
    var table = $('#docs').DataTable({
      "serverSide": false,
      "paging": false,
      "searching": false,
      "ordering": true,
      "dom": 't',
    // "lengthMenu": [ 10, 25, 50, 75, 100 ], // change number of records shown
    "columnDefs": [
        {
            "targets": [1,2,3,4],
            "orderable": false
        },
    ],
    });

    function exportTableToCSV($table, filename) {
          var $rows = $table.find('tr:has(td),tr:has(th)'),
              // Temporary delimiter characters unlikely to be typed by keyboard
              // This is to avoid accidentally splitting the actual contents
              tmpColDelim = String.fromCharCode(11), // vertical tab character
              tmpRowDelim = String.fromCharCode(0), // null character
              // actual delimiter characters for CSV format
              colDelim = '","',
              rowDelim = '"\r\n"',
              // Grab text from table into CSV formatted string
              csv = '"' + $rows.map(function (i, row) {
                  var $row = $(row), $cols = $row.find('td,th');
                  return $cols.map(function (j, col) {
                      var $col = $(col), text = $col.text();
                      return text.replace(/"/g, '""'); // escape double quotes
                  }).get().join(tmpColDelim);
              }).get().join(tmpRowDelim)
                  .split(tmpRowDelim).join(rowDelim)
                  .split(tmpColDelim).join(colDelim) + '"',
              csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);
            if (window.navigator.msSaveBlob) { // IE 10+
              window.navigator.msSaveOrOpenBlob(new Blob([csv], {type: "text/plain;charset=utf-8;"}), "csvname.csv")
            }
            else {
              $(this).attr({ 'download': filename, 'href': csvData, 'target': '_blank' });
            }
      }
      
      // This must be a hyperlink
    $("#xx").on('click', function (event) {
        exportTableToCSV.apply(this, [$('#extract'), 'export.csv']);
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
