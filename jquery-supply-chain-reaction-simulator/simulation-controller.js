/*
This a simulation of supply chain reaction.

The MIT License (MIT)

Copyright (c) 2016 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
