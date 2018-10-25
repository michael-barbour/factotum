function bubbleChart() {
    var width = 840,
        height = 500,
        maxRadius = 6,
        columnForColors = "gen_cat",
        columnForRadius = "num_prods";

    function chart(selection) {
        var data = selection.datum();
        var div = selection,
            svg = div.selectAll('svg');
        svg.attr('width', width).attr('height', height);

        var one = svg
            .append("text")
            .attr('x',80)
            .attr('y',20)
            .style('fill','green')
            .style('font-size','20px')
            .style("visibility", "hidden")
            .text("Level 1")
        var two = svg
            .append("text")
            .attr('x',347)
            .attr('y',20)
            .style('fill','green')
            .style('font-size','20px')
            .style("visibility", "hidden")
            .text("Level 2")

        var three = svg
            .append("text")
            .attr('x',640)
            .attr('y',20)
            .style('fill','green')
            .style('font-size','20px')
            .style("visibility", "hidden")
            .text("Level 3")

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

        var scaleRadius = d3v4.scaleLinear().domain([d3v4.min(data, function(d) {
            return +d[columnForRadius];
        }), d3v4.max(data, function(d) {
            return +d[columnForRadius];
        })]).range([2,10]);
        var colorCircles = d3v4.scaleOrdinal(d3v4.schemeCategory10)




        var forceXSeparate = d3v4.forceX(function (d){
            if(d.PUC_type === '1'){
                return 180
            } else if (d.PUC_type === '2'){
                return 420
            } else {
                return 660
            }
        }).strength(0.08)

        var forceXCombine = d3v4.forceX(width / 2).strength(0.05)

        var forceCollide = d3v4.forceCollide(function(d){
            return scaleRadius(d[columnForRadius]) + 5;
        })

        var simulation = d3v4.forceSimulation(data)
            // .force("charge", d3v4.forceManyBody().strength([-50]))
            .force('charge', d3v4.forceManyBody().strength(-8))
            .force("x", forceXCombine)
            .force("y", d3v4.forceY(height / 2).strength(0.05))
            .force("collide", forceCollide)
            .on("tick", ticked);

        function ticked(e) {
            node.attr("cx", function(d) {
                    return d.x;
                })
                .attr("cy", function(d) {
                    return d.y;
                });
        }
        d3v4.select("#split").on('click', function(){
            simulation
                .force("x", forceXSeparate)
                .alphaTarget(0.5)
                .restart()
            one
                .style("visibility", "visible")
            two
                .style("visibility", "visible")
            three
                .style("visibility", "visible")
        })

        d3v4.select("#combine").on('click', function(){
            simulation
                .force("x", forceXCombine)
                .alphaTarget(0.5)
                .restart()
            one
                .style("visibility", "hidden")
            two
                .style("visibility", "hidden")
            three
                .style("visibility", "hidden")
        })

        // var scaleRadius = d3v4.scaleLinear().domain([d3v4.min(data, function(d) {
        //     return +d[columnForRadius];
        // }), d3v4.max(data, function(d) {
        //     return +d[columnForRadius];
        // })]).range([11, 55])

        var node = svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr('r', function(d) {
                // alert(d)
                return scaleRadius(d[columnForRadius]) + 4
            })
            .style("fill", function(d) {
                return colorCircles(d[columnForColors])
            })
            .attr('stroke','black')
            .attr('stroke-width',0)
            .on("mouseover", function(d) {
                d3v4.select(this)
                  .transition()
                  .duration(500)
                  .attr('stroke-width',1)
                var matrix = this.getScreenCTM()
                    .translate(+ this.getAttribute("cx"), + this.getAttribute("cy"));
                tooltip.html("PUC Level: " + d.PUC_type + "<br><b>" + d.gen_cat + "-</b><br><b>-" + d.prod_fam + "-</b><br><b>-" + d.prod_type + "</b><br>" + "Product Count: " + d[columnForRadius])
                    .style("left", (window.pageXOffset + matrix.e + 15) + "px")
                    .style("top", (window.pageYOffset + matrix.f - 30) + "px");
                return tooltip.style("visibility", "visible");
            })
            .on("mouseout", function() {
                d3v4.select(this)
                  .transition()
                  .duration(1000)
                  .attr('stroke-width',0)
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
