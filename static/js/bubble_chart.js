function bubbleChart() {
    var width = 840,
        height = 420,
        maxRadius = 6,
        columnForColors = "PUC_type",
        columnForRadius = "num_prods";

    function chart(selection) {
        var data = selection.datum();
        var div = selection,
            svg = div.selectAll('svg');
        svg.attr('width', width).attr('height', height);

        var tooltip = selection
            .append("div")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("color", "white")
            .style("padding", "8px")
            .style("background-color", "#626D71")
            .style("border-radius", "6px")
            .style("text-align", "center")
            .style("font-family", "monospace")
            .style("width", "400px")
            .text("");

        var scaleRadius = d3.scaleSqrt().domain([d3.min(data, function(d) {
            return +d[columnForRadius];
        }), d3.max(data, function(d) {
            return +d[columnForRadius];
        })]).range([2,10]);
        var colorCircles = d3.scaleOrdinal(d3.schemeCategory10).domain([2,5]);
        var simulation = d3.forceSimulation(data)
            // .force("charge", d3.forceManyBody().strength([-50]))
            .force("x", d3.forceX(width / 2).strength(0.05))
            .force("y", d3.forceY(height / 2).strength(0.05))
            .force("collide", d3.forceCollide(function(d){
                return scaleRadius(d[columnForRadius]) + 4;
            }))
            .on("tick", ticked);

        function ticked(e) {
            node.attr("cx", function(d) {
                    return d.x;
                })
                .attr("cy", function(d) {
                    return d.y;
                });
        }


        // var scaleRadius = d3.scaleLinear().domain([d3.min(data, function(d) {
        //     return +d[columnForRadius];
        // }), d3.max(data, function(d) {
        //     return +d[columnForRadius];
        // })]).range([11, 55])

        var node = svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr('r', function(d) {
                // alert(d)
                return scaleRadius(d[columnForRadius]) + 3
            })
            .style("fill", function(d) {
                return colorCircles(d[columnForColors])
            })
            // .attr('transform', 'translate(' + [width / 2, height / 2] + ')')
            .on("mouseover", function(d) {
                tooltip.html("PUC Level: " + d[columnForColors] + "<br>" + d.gen_cat + "<br>" + d.prod_fam + "<br>" + d.prod_type + "<br>" + "Product Count: " + d[columnForRadius]);
                return tooltip.style("visibility", "visible");
            })
            .on("mousemove", function() {
                return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px");
            })
            .on("mouseout", function() {
                return tooltip.style("visibility", "hidden");
            });
    }

    chart.width = function(value) {
        if (!arguments.length) {
            return width;
        }
        width = value;
        return chart;
    };

    chart.height = function(value) {
        if (!arguments.length) {
            return height;
        }
        height = value;
        return chart;
    };


    chart.columnForColors = function(value) {
        if (!arguments.columnForColors) {
            return columnForColors;
        }
        columnForColors = value;
        return chart;
    };

    chart.columnForRadius = function(value) {
        if (!arguments.columnForRadius) {
            return columnForRadius;
        }
        columnForRadius = value;
        return chart;
    };

    return chart;
}
