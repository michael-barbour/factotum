nv.addGraph(function () {
    var chart = nv.models.lineChart(x_is_date=true)
        .color(d3.scale.category10().range())
        .x(function(d) {return d3.time.format("%Y-%m-%d").parse(d['x']);});
    chart.xAxis
        .axisLabel('Date')
        .tickFormat(function(d) {
            return d3.time.format('%m/%d/%y')(new Date(d))
        });
    chart.xScale(d3.time.scale());
    chart.yAxis
        .tickFormat(d3.format(',.0f'));
    d3.select('#lineChart svg')
        .datum(data_lineChart)
        .transition().duration(500)
        .attr('height', 350)
        .call(chart);
    return chart;
});

