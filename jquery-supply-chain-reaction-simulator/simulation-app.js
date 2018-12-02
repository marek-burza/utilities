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

function SimulatorApp(configuration){
  this.configuration = configuration;
  this.MONTH = 4 * 7 * 24 * 60 * 60 * 1000;

  this.utilityMonthOffset = function(date, offset){
    var result = new Date(date);
    result.setTime(result.getTime() + offset * this.MONTH);
    return(result);
  };

  this.utilityValid = function(value){
    return(!(undefined === value || null == value));
  };

  this.app = function(){
    var view = new SimulatorView();
    var controller = new SimulatorController();
    var model = new SimulatorModel(configuration);
    controller.inject(this, model, view);
    view.inject(this, model, controller);
    model.inject(this, view);
    model.refresh();
  };

  this.initialize = function(){
    var simulator = this;
    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(function(){simulator.app();});
  };
}
