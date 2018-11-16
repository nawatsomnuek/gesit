var w = 500,
	h = 500;

var colorscale = d3.scale.category10();

//Legend titles
var LegendOptions = ['Group1','Group2','Group3'];

//Data
var d = [
		  [
			{axis:"INT102",value:3.5},
			{axis:"INT105",value:3.6},
			{axis:"INT106",value:3.3},
			{axis:"INT302",value:3.7},
			{axis:"INT303",value:3.9},
		  ],[
			{axis:"INT102",value:1.34},
			{axis:"INT105",value:1.91},
			{axis:"INT106",value:1.93},
			{axis:"INT302",value:1.88},
			{axis:"INT303",value:2.41},
		  ],[
			{axis:"INT102",value:3.34545455},
			{axis:"INT105",value:1.63636364},
			{axis:"INT106",value:3.19090909},
			{axis:"INT302",value:1.83636364},
			{axis:"INT303",value:2.45454545},
		  ]
		];

//Options for the Radar chart, other than default
var mycfg = {
  w: w,
  h: h,
  maxValue: 3.7195122,
  levels: 0,
  ExtraWidthX: 300
}

//Call function to draw the Radar chart
//Will expect that data is in %'s
RadarChart.draw("#chart", d, mycfg);

////////////////////////////////////////////
/////////// Initiate legend ////////////////
////////////////////////////////////////////

var svg = d3.select('#body')
	.selectAll('svg')
	.append('svg')
	.attr("width", w+300)
	.attr("height", h)

//Create the title for the legend
var text = svg.append("text")
	.attr("class", "title")
	.attr('transform', 'translate(90,0)') 
	.attr("x", w - 70)
	.attr("y", 10)
	.attr("font-size", "12px")
	.attr("fill", "#404040")
	.text("Center value of Each Group (Programming Field 55)");
		
//Initiate Legend	
var legend = svg.append("g")
	.attr("class", "legend")
	.attr("height", 100)
	.attr("width", 200)
	.attr('transform', 'translate(90,20)') 
	;
	//Create colour squares
	legend.selectAll('rect')
	  .data(LegendOptions)
	  .enter()
	  .append("rect")
	  .attr("x", w - 65)
	  .attr("y", function(d, i){ return i * 20;})
	  .attr("width", 10)
	  .attr("height", 10)
	  .style("fill", function(d, i){ return colorscale(i);})
	  ;
	//Create text next to squares
	legend.selectAll('text')
	  .data(LegendOptions)
	  .enter()
	  .append("text")
	  .attr("x", w - 52)
	  .attr("y", function(d, i){ return i * 20 + 9;})
	  .attr("font-size", "11px")
	  .attr("fill", "#737373")
	  .text(function(d) { return d; })
	  ;	