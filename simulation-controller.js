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

function SimulatorController(){
  this.inject = function(simulator, model, view){
    this.simulator = simulator;
    this.model = model;
    this.view = view;
  };

  this.salesChanged = function(){
    var sku = this.view.getSKU();
    var sales = this.view.getSales();
    this.model.setSales(sku, sales);
  };

  this.demandChanged = function(){
    var sku = this.view.getSKU();
    var ahead = this.view.getAhead();
    var demand = this.view.getDemand();
    this.model.setDemand(sku, ahead, demand);
  };

  this.incomingChanged = function(){
    var sku = this.view.getSKU();
    var incoming = this.view.getIncoming();
    this.model.setIncoming(sku, incoming);
  };

  this.advance = function(){
	  this.model.advance();
  };
}
