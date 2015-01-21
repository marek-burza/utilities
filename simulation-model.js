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

function SimulatorModel(configuration){
  this.configuration = configuration;
  this.INDEX_DATE = 0;
  this.INDEX_SALES = 1;
  this.INDEX_SUPPLY = 2;
  this.INDEX_VIRTUAL = 3;
  this.INDEX_DEMAND = 4;
  this.INDEX_BIAS = 5;
  this.INDEX_FA = 6;
  this.INDEX_STOCK = 7;
  this.INDEX_EXCESS = 8;
  this.FAINT_RED = "#FFDDDD";

  this.inject = function(simulator, view){
    this.simulator = simulator;
    this.view = view;
    this.initialize();
  };

  this.getLead = function(){
    return(this.configuration.lead);
  };

  this.getForesight = function(){
    return(this.configuration.foresight);
  };

  this.getMaximumVolume = function(){
    return(this.configuration.maximum);
  }

  this.getPortfolio = function(){
    return(this.configuration.default.length);
  };

  this.getDefaultVolume = function(sku){
    return(this.configuration.default[sku]);
  }

  this.initialize = function(){
	  // Now
	  var date2013 = new Date("2013");
    var date2014 = new Date("2014");
    this.now = new Date();
    this.now.setTime((date2013.getTime() + date2014.getTime()) / 2);

	  // Portfolio
    this.portfolio = [];
    for(var i = 0; i < this.getPortfolio(); i++){
      var demand = [];
      for(var j = 0; j < this.getForesight() + 1; j++){
        demand[j] = this.getDefaultVolume(i);
      }
      this.portfolio[i] = {sales:this.getDefaultVolume(i), supply: this.getDefaultVolume(i), demand: demand, incoming: this.getDefaultVolume(i)};
    }

    this.data = new google.visualization.DataTable();
    this.data.addColumn({type:"date",   label:"Week"});
    this.data.addColumn({type:"number", label:"Sales"});
    this.data.addColumn({type:"number", label:"Supply"});
    this.data.addColumn({type:"string", role:"style"});
    this.data.addColumn({type:"number", label:"Demand"});
    this.data.addColumn({type:"number", label:"Bias"});
    this.data.addColumn({type:"number", label:"FA  "});
    this.data.addColumn({type:"number", label:"Stock"});
    this.data.addColumn({type:"number", label:"Excess"});

    var volume = 0;
    for(var i = 0; i < this.getPortfolio(); i++){
      volume += this.getDefaultVolume(i);
    }
    var origin = this.simulator.utilityMonthOffset(this.now, -this.getLead());
    var lead = this.simulator.utilityMonthOffset(this.now, this.getLead());
    for(var i = 0; i < this.getLead() + this.getForesight() + 1; i++){
      var at = this.simulator.utilityMonthOffset(origin, i);
      var none = undefined;
      var entry = [at, none, none, this.FAINT_RED, none, none, none, none, none];
      if(this.now.getTime() == at.getTime()){
        entry[this.INDEX_SALES] = volume;
      }
      if(at.getTime() <= lead.getTime()){
        entry[this.INDEX_VIRTUAL] = "#FF0000";
      }
      entry[this.INDEX_SUPPLY] = volume;
      entry[this.INDEX_DEMAND] = volume;
      this.data.addRow(entry);
    }
  };

  this.getNow = function(){
	  return(this.now);
  };

  this.getSales = function(sku){
	  return(this.portfolio[sku].sales);
  };

  this.getSupply = function(sku){
	  return(this.portfolio[sku].supply);
  };

  this.getDemand = function(sku, ahead){
	  return(this.portfolio[sku].demand[ahead]);
  };

  this.getIncoming = function(sku){
	  return(this.portfolio[sku].incoming);
  };

  this.setSales = function(sku, sales){
    this.portfolio[sku].sales = sales;
    var total = 0;
    for(var i = 0; i < this.getPortfolio(); i++){
      total += this.portfolio[i].sales;
    }
    if(this.get(this.now, this.INDEX_SALES) != total){
      this.set(this.now, this.INDEX_SALES, total);
      this.refresh();
    }
  };

  this.setDemand = function(sku, ahead, demand){
	  var changed = false;
    this.portfolio[sku].demand[ahead] = demand;
    var totalDemand = 0;
    for(var i = 0; i < this.getPortfolio(); i++){
      totalDemand += this.portfolio[i].demand[ahead];
    }
    var then = this.simulator.utilityMonthOffset(this.now, ahead);
    if(this.get(then, this.INDEX_DEMAND) != totalDemand){
      this.set(then, this.INDEX_DEMAND, totalDemand);
	    changed = true;
	  }
    if(0 == ahead){
  	  this.portfolio[sku].supply = demand;
  	}
      var then = this.simulator.utilityMonthOffset(this.now, this.getLead() + ahead);
      var totalSupply = 0;
      for(var i = 0; i < this.getPortfolio(); i++){
        totalSupply += this.portfolio[i].demand[ahead];
      }
      if(this.get(then, this.INDEX_SUPPLY) != totalSupply){
  	    this.set(then, this.INDEX_SUPPLY, totalSupply);
  	    changed = true;
  	  }
	  if(changed){
      this.refresh();
    }
  };

  this.setIncoming = function(sku, incoming){
    this.portfolio[sku].incoming = incoming;
  };

  this.getChartData = function(){
    return(this.data);
  };

  this.get = function(at, index){
    for(var i = 0; i < this.data.getNumberOfRows(); i++){
      if(this.data.getValue(i, this.INDEX_DATE).getTime() == at.getTime()){
        return(this.data.getValue(i, index));
      }
    }
    return(undefined);
  };

  this.set = function(at, index, value){
    for(var i = 0; i < this.data.getNumberOfRows(); i++){
      if(this.data.getValue(i, this.INDEX_DATE).getTime() == at.getTime()){
        this.data.setValue(i, index, value);
      }
    }
  };

  this.advance = function(){
    var newSales = 0;
    var newSupply = 0;
	  var newDemand = 0;
	  for(var sku = 0; sku < this.getPortfolio(); sku++){
      var demand = this.portfolio[sku].demand;
		  newSales += this.portfolio[sku].sales;
      newSupply += demand[1];
      this.portfolio[sku].supply = demand[1];
      demand.push(this.portfolio[sku].incoming);
      newDemand += this.portfolio[sku].incoming;
      demand.shift();
    }
    for(var i = 0; i < this.data.getNumberOfRows(); i++){
  	  if(this.data.getValue(i, this.INDEX_DATE).getTime() == this.now.getTime()){
        this.data.setValue(i + 1 + this.getLead(), this.INDEX_SUPPLY, newSupply);
        this.data.setValue(i + 1 + this.getLead(), this.INDEX_VIRTUAL, "#FF0000");
        this.data.setValue(i + 1,                  this.INDEX_SALES,  newSales);
        break;
      }
    }
    var reSupply = 0;
    for(var sku = 0; sku < this.getPortfolio(); sku++){
      reSupply += this.portfolio[sku].demand[this.getLead()];
    }
    this.data.addRow([this.simulator.utilityMonthOffset(this.now, this.getForesight() + 1), undefined, reSupply, this.FAINT_RED, newDemand, undefined, undefined, undefined, undefined]);
    this.now = this.simulator.utilityMonthOffset(this.now, 1);
    this.refresh();
  };

  this.recalculate = function(){
    var horizon = this.simulator.utilityMonthOffset(this.now, this.getForesight() + 1);
    var stock = 0;
    for(var i = 0; i < this.data.getNumberOfRows(); i++){
      var at = this.data.getValue(i, this.INDEX_DATE);
      var sales = this.data.getValue(i, this.INDEX_SALES);
      if(at.getTime() < horizon.getTime()){
        var supply = this.data.getValue(i, this.INDEX_SUPPLY);
        stock += supply;
        if(this.simulator.utilityValid(sales)){
          stock -= sales;
        }
        this.data.setValue(i, this.INDEX_STOCK, stock);
      }
      if(this.now.getTime() < at.getTime()){
    	  var demand = this.data.getValue(i, this.INDEX_DEMAND);
    	  stock -= demand;
      }
      if(at.getTime() == this.now.getTime()){
        var fa = 0;
        if(!this.configuration.fa){
          fa = undefined;
        }else{
          var count = 0;
          for(var j = 0; j < this.getPortfolio(); j++){
            if(0 != this.portfolio[j].sales){
              fa += /*Math.abs*/(this.portfolio[j].sales - this.portfolio[j].demand[0]) / this.portfolio[j].sales;
              count++;
            }
          }
          fa /= this.getPortfolio();
        }
        this.data.setValue(i, this.INDEX_FA, fa);
      }
      if(at.getTime() <= this.now.getTime()){
        if(this.simulator.utilityValid(sales)){
          var demand = this.data.getValue(i, this.INDEX_DEMAND);
          var bias = (demand - sales) / demand;
          this.data.setValue(i, this.INDEX_BIAS, bias);
        }
        if(this.simulator.utilityValid(this.data.getValue(i, this.INDEX_DEMAND))){
          var plan = 0;
          for(var j = 0; j < this.getForesight(); j++){
            plan += this.data.getValue(i + j, this.INDEX_DEMAND);
          }
          var excess = stock - plan;
          this.data.setValue(i, this.INDEX_EXCESS, excess);
        }
      }
    }
  };

  this.refresh = function(){
	  this.recalculate();
	  this.view.refresh();
  };
}
