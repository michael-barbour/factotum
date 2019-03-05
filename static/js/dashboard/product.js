$(document).ready(function () {
    var table = $('#products').DataTable({
        "serverSide": false,
        "paging": true,
        "searching": true,
        "ordering": true,
        dom: "<'row'<'col-md-4 form-inline'l><'col-md-4 form-inline'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'i><'col-sm-7'p>>", // order the control divs
        "columns": [
            {"width": "50%"},
            {"width": "20%"},
            {"width": "30%"}
        ]
    });
});

$('#id_tags').addClass('taggit-labels taggit-list')

        $(document).ready(function($) {
            var inputs = $(this).find(".taggit-labels + input")[0]
            var tagList = inputs.value.split(", ")
            tagList.indexOf("") === -1 ? tagList.push("") : tagList
            $("#tag_submit").attr('disabled', 'disabled');
            $(".taggit-tag").click(function(){
                var tag = $(this).text()
                var curList = $('.taggit-labels + input')[0].value.split(", ")
                curList.indexOf("") === -1 ? curList.push("") : curList
                if (curList.includes(tag)){
                    curList = curList.filter(function(e) { return e !== tag })
                }else {
                    curList.push($(this).text())
                }
                if (curList.sort().join(',') === tagList.sort().join(',')){
                    $("#tag_submit").attr('disabled', 'disabled');
                }else{
                    $("#tag_submit").removeAttr("disabled");
                }
            })
        });