var width = 1000;
var height = 900;
var r1 = height / 2;
var r0 = r1 - 110;
var outerRadius = 250
var innerRadius = 220
var formatPercent = d3.format(".1%");
 
var arc = d3.svg.arc()
  .innerRadius(innerRadius)
  .outerRadius(outerRadius);
 
var layout = d3.layout.chord()
  .padding(.04);
 
var path = d3.svg.chord()
  .radius(innerRadius);
 
function drawDiagram(year) {
  $("svg").remove();
  var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height) 
    .append("g")
    .attr("id", "circle")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
  
  svg.append("circle")
    .attr("r", outerRadius);
  
  d3.csv("/static/img/" + year + "-standings.csv", function(cities) {
    d3.json("static/img/" + year + ".json", function(matrix) {
      layout.matrix(matrix);
      var group = svg.selectAll(".group")
        .data(layout.groups)
        .enter().append("g")
        .attr("class", "group")
        .on("mouseover", mouseover);

      var groupPath = group.append("path")
        .attr("id", function(d, i) { return "group" + i; })
        .attr("d", arc)
        .style("fill", function(d, i) { return cities[i].color; });
     
      // Add a text label.
      var groupText = group.append("svg:text")
        .attr("x", 6)
        .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
        .attr("dy", ".35em")
        .style("font-family", "helvetica, arial, sans-serif")
        .style("font-size", "12px")
        .attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
        .attr("transform", function(d) {
          return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
              + "translate(" + (r0 - 75 ) + ")"
              + (d.angle > Math.PI ? "rotate(180)" : "");
        })
        .attr("class", function(d) {
          if(cities[d.index].wins > 100) {
            return "winning-100";
          } else if (cities[d.index].wins > 90) {
            return "winning-90";
          } else if (cities[d.index].wins > 80) {
            return "winning-80";
          } else if (cities[d.index].wins > 70) {
            return "winning-70";
          } else if (cities[d.index].wins > 60) {
            return "winning-60";
          }
        })
        .attr("fill", function(d) {
          if(cities[d.index].ws > 0) {
            return "gold";
          } else if (cities[d.index].ws < 0) {
            return "red";
          }
        })
        .text(function(d) { 
          return cities[d.index].wins + " -  " + cities[d.index].name;
        });

        var groupLogo = group.append("svg:image")
        .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
        .attr("transform", function(d) {
          var offset = cities[d.index].name.length;
          offset = offset * 6.5;

          return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
              + "translate(" + (d.angle > Math.PI ? (r0 + 105) : (r0 + 85)) + "," +  (d.angle > Math.PI ? 15 : -15) + ")"
              + (d.angle > Math.PI ? "rotate(180)" : "");
        })
        .attr('width', 30)
        .attr('height', 30)
        .attr("xlink:href", function(d) {
          return cities[d.index].images;
      });
      var chord = svg.selectAll(".chord")
        .data(layout.chords)
        .enter().append("path")
        .attr("class", "chord")
        .style("fill", function(d) { return cities[d.source.index].color; })
        .attr("d", path)
        .on("mouseover", function (d) {
          id = "trade";
          d3.select("#tooltip")
            .style("visibility", "visible")
            .html("<div id='" + id + "'" + chordTip(d, id) + "</div>")
            .style("top", function () { return (d3.event.pageY - 100)+"px"})
            .style("left", function () { return (d3.event.pageX - 100)+"px";})
        })
        .on("mouseout", function (d) {
          d3.select("#tooltip")
            .style("visibility", "hidden");
          });

      function chordTip (d, id) {
        var source = cities[d.source.index].name;
        var target = cities[d.target.index].name
        var year = $("#year").text(); 
        var val = 
          $.get("api/" + year + "/" + source + "/" + target, function(data, status){
            trades = data.trades;
            var text = "<ul>";
            for (var i = 0; i < trades.length; i++){
              if(i > 0 && trades[i].note == trades[i-1].note) {
                continue;
              }
              text += "<li>";
              text += trades[i].note;
              text += "</li>";
            }
            text += "</ul>";
            $("#" + id).html(text);
            embedPlayers(trades[0].transaction_id, year);
          });
        return "Loading";
      }

      function embedPlayers(transaction_id, year) {
        $.get("api/transaction/" + transaction_id, function(data, status){
          data = data.trades;
          console.log(data);
          if(data.length != 2){
            $('embed#player-1').hide();
            $('embed#player-2').hide();
            return;
          }
          $('embed#player-1').show();
          $('embed#player-2').show();
          var player_url = "http://m.mlb.com/player/" + data[0].player_id + "?year=" + year;
          var parent = $('embed#player-1').parent();
          var newElement = "<embed src='" + player_url +  "' id='player-1'>";
          $('embed#player-1').remove();
          parent.append(newElement);
          player_url = "http://m.mlb.com/player/" + data[1].player_id + "?year=" + year;
          parent = $('embed#player-2').parent();
          newElement = "<embed src='" + player_url +  "' id='player-2'>";
          $('embed#player-2').remove();
          parent.append(newElement);
        });
      }
      
      //Team Mouseover
      function mouseover(d, i) {
        chord.classed("fade", function(p) {
          return p.source.index != i && p.target.index != i;
        });
      }
    });
  });
}
drawDiagram(2015);
$(".slider").on("change", function(){
  drawDiagram(this.value)
});

function updateTextInput(val) {
  $("#year").text(val); 
}