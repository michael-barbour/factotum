// Load hover buttons
function renderDataTable(boolComp, boolHab, fsid) {
    function renderTitle(data, type, row, meta) {
        if (row.fileext == ".pdf") {
            var icon = "fa-file-pdf";
        } else {
            var icon = "fa-file";
        }
        if (row.matched) {
            return [
                "<a ",
                "href='/media/" + fsid + "/pdf/document_" + row.id + row.fileext + "' ",
                "title='Link to document_" + row.id + row.fileext + "' ",
                "target='_blank'",
                ">",
                "<span class='fa " + icon + " mr-2'></span>",
                "</a>",
                "<a ",
                "href='/datadocument/" + row.id + "/' ",
                "title='Link to document detail'",
                ">",
                row.title,
                "</a>"
            ].join("");
        } else {
            return row.title;
        }
    }
    function renderMatched(data, type, row, meta) {
        if (row.matched) {
            return "<div class='text-secondary text-center'><span class='fa fa-check'></span></div>";
        } else {
            return [
                "<div class='text-center'>",
                "<a class='btn btn-sm btn-outline-secondary hover-danger' title='Delete' ",
                "href ='datadocument/delete/" + row.id + "/'",
                ">",
                "<span class='fa fa-trash'></span>",
                "</a>",
                "</div>"
            ].join("");
        }
    }
    function renderExtracted(data, type, row, meta) {
        if (row.extracted) {
            return "<div class='text-secondary text-center'><span class='fa fa-check'></span></div>";
        } else {
            return "<div class='text-secondary text-center'><span class='fa fa-times'></span></div>";
        }
    }

    function renderHab(data, type, row, meta) {
        return [
            "<div class='text-center'>",
            "<a class='btn btn-sm btn-outline-secondary hover-success' title='Edit/inspect habits and practices' ",
            "href ='habitsandpractices/" + row.id + "/'",
            ">",
            "<span class='fa fa-edit'></span>",
            "</a>",
            "</div>"
        ].join("");
    }
    function renderProd(data, type, row, meta) {
        if (row.product_id) {
            return "<div class='text-center'><a href='/product/" + row.product_id + "/'>" + row.product_title + "</a></div>";
        } else {
            return "<div class='text-secondary text-center'><span class='fa fa-times'></span></div>";
        }
    }
    if (boolComp) {
        var columns = [
            { "data": "title", "render": renderTitle },
            { "data": "matched", "render": renderMatched },
            { "data": "extracted", "render": renderExtracted },
            { "data": "product", "render": renderProd }
        ];
    } else if (boolHab) {
        var columns = [
            { "data": "title", "render": renderTitle },
            { "data": "matched", "render": renderMatched },
            { "data": "edit", "render": renderHab },
        ];
    } else {
        var columns = [
            { "data": "title", "render": renderTitle },
            { "data": "matched", "render": renderMatched },
            { "data": "extracted", "render": renderExtracted },
        ];
    }
    $('#docs').dataTable({
        "ajax": "./documents_table/",
        "columns": columns
    });
}
function renderDonut(id, part, total) {
    // http://bl.ocks.org/mbostock/5100636
    var tau = 2 * Math.PI;
    var arc = d3.arc()
        .innerRadius(15)
        .outerRadius(20)
        .startAngle(0);
    var svg = d3.select("#" + id),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    var background = g.append("path")
        .datum({ endAngle: tau })
        .style("fill", "#CCCCCC")
        .attr("d", arc);
    var foreground = g.append("path")
        .datum({ endAngle: 0.0 * tau })
        .style("fill", "#3B3B3B")
        .attr("d", arc);
    d3.timeout(function () {
        foreground.transition()
            .duration(1000)
            .attrTween("d", arcTween((part / total) * tau));
    }, 500);
    function arcTween(newAngle) {
        return function (d) {
            var interpolate = d3.interpolate(d.endAngle, newAngle);
            return function (t) {
                d.endAngle = interpolate(t);
                return arc(d);
            };
        };
    }
}
$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    })
    var tableData = JSON.parse(document.getElementById('tabledata').textContent);
    renderDataTable(tableData.boolComp, tableData.boolHab, tableData.fsid);
    renderDonut("matcheddonut", tableData.nummatched, tableData.numregistered);
    renderDonut("extracteddonut", tableData.numextracted, tableData.numregistered);
});