var total_observations = 0,a=0,b=0;

$.each(data.clusters, function(i, val){
  a = getTotal(i,0);
  b = getTotal(i,1);
  total_observations += (a+b);

  var cluster = d3.select("#clusters").append("div")
  .attr("id", "cluster"+i)
  .attr("class", "col-md-12");

  cluster.append("h2").text("Cluster "+(i+1)+", Total : "+getTotal(i, -1));

  var correct = cluster
  .append("div")
  .attr("class", "col-md-offset-1 col-md-5 correct well")

  correct.append("p").text("Standards");
  correct.append("svg").attr("height", 500);
  correct.append("p").text("Total : "+a).style("text-align", "center");

  var anomaly = cluster
  .append("div")
  .attr("class", "col-md-offset-1 col-md-5 anomaly well")

  anomaly.append("p").text("Anomalies with "+data.N+" %");
  anomaly.append("svg").attr("height", 500);
  anomaly.append("p").text("Total : "+b).style("text-align", "center");


  nv.addGraph(function() {
    var chart = nv.models.pieChart()
        .x(function(d) { return d.label })
        .y(function(d) { return d.value })
        .showLabels(true)     
        .labelThreshold(.05)  
        .labelType("percent") 
        .donut(true)          
        .donutRatio(0.35)   
        .color(["#4183D7","#59ABE3","#81CFE0","#52B3D9","#446CB3","#C5EFF7","#22A7F0","#3498DB","#2C3E50","#19B5FE","#336E7B","#22313F","#6BB9F0","#1E8BC3","#3A539B","#34495E","#67809F","#2574A9","#1F3A93","#89C4F4","#4B77BE","#5C97BF","#E4F1FE"])
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
        .color(["#DB0A5B","#F64747","#F1A9A0","#D2527F","#E08283","#F62459","#E26A6A","#D24D57","#F22613","#D91E18","#96281B","#EF4836","#D64541","#C0392B","#CF000F","#E74C3C"]) 
        ;

      d3.select("#cluster"+i+" .anomaly svg")
          .datum(getData(i, 1))
          .transition().duration(350)
          .call(chart);

    return chart;
  });
});

d3.select("#clusters").append("div").append("h4")
  .attr("class", "col-md-12")
  .attr("id", "total_observations")
  .text("Total of observations : "+total_observations);

function getData(i, flag) {
  return  flag == 1 ? data.clusters[i].stats[0].anomalies : data.clusters[i].stats[1].corrects;
}

function getTotal(i, flag){
  var res=0;
  if(flag != -1){
    var d = flag == 1 ? data.clusters[i].stats[0].anomalies : data.clusters[i].stats[1].corrects;
    $.each(d, function(i, val){
      res += val.value;
    });
  }
  else
    res = getTotal(i, 1) + getTotal(i, 0);
  return res;
}