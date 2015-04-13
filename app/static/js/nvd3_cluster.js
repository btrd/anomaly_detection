$.each(data.clusters, function(i, val){
  var cluster = d3.select("#result").append("div")
  .attr("id", "cluster"+i)
  .attr("class", "span9");

  cluster.append("h2").text("Cluster "+(i+1));

  var correct = cluster
  .append("div")
  .attr("class", "span4 correct")

  correct.append("p").text("Normals");
  correct.append("svg");

  var anomaly = cluster
  .append("div")
  .attr("class", "span4 anomaly")

  anomaly.append("p").text("Anomalies with "+data.N+" %");
  anomaly.append("svg");


  nv.addGraph(function() {
    var chart = nv.models.pieChart()
        .x(function(d) { return d.label })
        .y(function(d) { return d.value })
        .showLabels(true)     
        .labelThreshold(.05)  
        .labelType("percent") 
        .donut(true)          
        .donutRatio(0.35)    
        ;

      d3.select("#cluster"+i+" .correct svg")
          .datum(getData(i, 0))
          .transition().duration(350)
          .call(chart);

    return chart;
  });

  nv.addGraph(function() {
    var chart = nv.models.pieChart()
        .x(function(d) { return d.label })
        .y(function(d) { return d.value })
        .showLabels(true)     
        .labelThreshold(.05)  
        .labelType("percent") 
        .donut(true)          
        .donutRatio(0.35)     
        ;

      d3.select("#cluster"+i+" .anomaly svg")
          .datum(getData(i, 1))
          .transition().duration(350)
          .call(chart);

    return chart;
  });
});

function getData(i, flag) {
  return  flag == 1 ? data.clusters[i].stats[0].anomalies : data.clusters[i].stats[1].corrects;
}