/*
This a simulation of supply chain reaction.

This code is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This code is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with code. If not, see <http://www.gnu.org/licenses/>.
*/

function SimulatorView(){
  this.HALF = 6;

  this.inject = function(simulator, model, controller){
    this.simulator = simulator;
    this.model = model;
    this.controller = controller;
    this.initialize();
  };

  this.getSales = function(){
    return($("#sales").slider("value"));
  };

  this.getDemand = function(){
    return($("#demand").slider("value"));
  };

  this.getIncoming = function(){
    return($("#incoming").slider("value"));
  };

  this.getSKU = function(){
	  return($("#sku").spinner("value"));
  };

  this.getAhead = function(){
	  return($("#ahead").spinner("value"));
  };

  this.updateSliderLabel = function(ui){
    var value = ui.value;
    var target = ui.handle;
    var tooltip = "<div class='tooltip' style='font-size:6pt; color:white;'>" + value + "</div>";
    $(target).html(tooltip);
  };

  this.salesChanged = function(event, ui){
    this.updateSliderLabel(ui);
    this.controller.salesChanged();
  };

  this.demandChanged = function(event, ui){
    this.updateSliderLabel(ui);
    this.controller.demandChanged();
  };

  this.incomingChanged = function(event, ui){
    this.updateSliderLabel(ui);
    this.controller.incomingChanged();
  };

  this.initialize = function(){
    var view = this;
	  // Dashboard
    $(function(){
      $("#sku").spinner({
        min: 0,
        max: view.model.getPortfolio() - 1,
        value: 0,
        stop: function(){view.refresh();},
        change: function(){view.refresh();}
      }).val(0);
      $("#sku").bind("keydown", function(event){event.preventDefault();});
      $("#sku").focus(function(){$(this).blur();});
      $("#ahead").spinner({
        min: 0,
        max: view.model.getForesight(),
        value: 0,
        stop: function(){view.refresh();},
        change: function(){view.refresh();}
      }).val(0);
      $("#ahead").bind("keydown", function(event){event.preventDefault();});
      $("#ahead").focus(function(){$(this).blur();});
      $("#sales").slider({
        orientation: "vertical",
        range: "min",
        step: 5,
        max: view.model.getMaximumVolume(),
        value: view.model.getDefaultVolume(0),
        slide: function(event, ui){view.salesChanged(event, ui);},
        change: function(event, ui){view.salesChanged(event, ui);}
      });
      $("#demand").slider({
        orientation: "vertical",
        range: "min",
        step: 5,
        max: view.model.getMaximumVolume(),
        value: view.model.getDefaultVolume(0),
        slide: function(event, ui){view.demandChanged(event, ui);},
        change: function(event, ui){view.demandChanged(event, ui);}
      });
      $("#incoming").slider({
        orientation: "vertical",
        range: "min",
        step: 5,
        max: view.model.getMaximumVolume(),
        value: view.model.getDefaultVolume(0),
        slide: function(event, ui){view.incomingChanged(event, ui);},
        change: function(event, ui){view.incomingChanged(event, ui);}
      });
      $("#advance").button().click(function(event){
        view.controller.advance();
        event.preventDefault();
      });
    });
    // Chart
    this.options = {
      title: "Simulation",
      vAxes: {0: {format:"#", title:"Volume"}, 1: {format:"#%", title: "Percentage", viewWindow:{min:-1, max:1}}},
      hAxis: {title: "Month", viewWindow:{}},
      series: {
        0: {type: "bars", targetAxisIndex:0},
        1: {type: "bars", targetAxisIndex:0},
        2: {type: "bars", targetAxisIndex:0},
        3: {type: "line", targetAxisIndex:1},
        4: {type: "line", targetAxisIndex:1},
        5: {type: "line", targetAxisIndex:0},
        6: {type: "line", targetAxisIndex:0}
      },
      colors: ["#0000FF", "#FF0000", "#00FF00", "#FF6600", "#FFFF00", "#00FFFF", "#FF00FF"]
    };
    this.chart = new google.visualization.LineChart(document.getElementById("chart"));
  };

  this.refresh = function(){
    var sku = this.getSKU();
    var ahead = this.getAhead();
    var sales = this.model.getSales(sku);
    if($("#sales").slider("value") != sales){
      $("#sales").slider("value", sales);
    }
    var demand = this.model.getDemand(sku, ahead);
    if($("#demand").slider("value") != demand){
      $("#demand").slider("value", demand);
    }
    var incoming = this.model.getIncoming(sku);
    if($("#incoming").slider("value") != incoming){
      $("#incoming").slider("value", incoming);
    }
    var now = this.model.getNow();
    this.options.hAxis.viewWindow.min = this.simulator.utilityMonthOffset(now, -(this.HALF + 1));
    this.options.hAxis.viewWindow.max = this.simulator.utilityMonthOffset(now,  (this.HALF + 1));
	  this.chart.draw(this.model.getChartData(), this.options);
  };
}