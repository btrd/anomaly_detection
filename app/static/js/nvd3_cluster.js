$.each(data.clusters, function(i, val){
  var cluster = d3.select("#clusters").append("div")
  .attr("id", "cluster"+i)
  .attr("class", "col-md-12");

  cluster.append("h2").text("Cluster "+(i+1)+", Total : "+getTotal(i, -1));

  var correct = cluster
  .append("div")
  .attr("class", "col-md-offset-1 col-md-5 correct well")

  correct.append("p").text("Normals");
  correct.append("svg").attr("height", 300);
  correct.append("p").text("Total : "+getTotal(i, 0)).style("text-align", "center");

  var anomaly = cluster
  .append("div")
  .attr("class", "col-md-offset-1 col-md-5 anomaly well")

  anomaly.append("p").text("Anomalies with "+data.N+" %");
  anomaly.append("svg").attr("height", 300);
  anomaly.append("p").text("Total : "+getTotal(i, 1)).style("text-align", "center");


  nv.addGraph(function() {
    var chart = nv.models.pieChart()
        .x(function(d) { return d.label })
        .y(function(d) { return d.value })
        .showLabels(true)     
        .labelThreshold(.05)  
        .labelType("percent") 
        .donut(true)          
        .donutRatio(0.35)   
        .color(["#E4F1FE","#4183D7","#59ABE3","#81CFE0","#52B3D9","#446CB3","#C5EFF7","#22A7F0","#3498DB","#2C3E50","#19B5FE","#336E7B","#22313F","#6BB9F0","#1E8BC3","#3A539B","#34495E","#67809F","#2574A9","#1F3A93","#89C4F4","#4B77BE","#5C97BF"])
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
        .color(["#FDE3A7","#F89406","#EB9532","#E87E04","#F4B350","#F2784B","#EB974E","#F5AB35","#D35400","#F39C12","#F9690E","#F9BF3B","#F27935","#E67E22"]) 
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