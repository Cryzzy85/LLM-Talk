var layout;
var tooltip;
var wordGroup;

function generateWordCloud(document) {
    d3.json("/static/data/word_freq.json").then(function(data) {
        var wordcloud = d3.select("#wordcloud");

        // Clear the existing word cloud
        wordcloud.html("");

        var width = wordcloud.node().getBoundingClientRect().width;
        var height = wordcloud.node().getBoundingClientRect().height;

        layout = d3.layout.cloud()
            .size([width, height])
            .words(Object.entries(data[document]).map(function(d) {
                return {text: d[0], size: d[1]};
            }))
            .padding(5)
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", draw);

        var svg = wordcloud
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        wordGroup = svg.append("g");

        svg.call(d3.zoom().on("zoom", function() {
            wordGroup.attr("transform", d3.event.transform);
        }));

        tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        layout.start();

    }).catch(function(error) {
        console.log("Error: " + error);
    });
}

function draw(words) {
    wordGroup.append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Quicklime, sans-serif")
        .style("fill", "lightblue")  // Set color of text
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; })
        .on("mouseover", function(d) {  // on mouse in
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            tooltip.html(d.text + "<br/>"  + d.size)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {  // on mouse out
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        });
}


