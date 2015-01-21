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
