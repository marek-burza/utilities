Simulator of Supply Chain Reaction
===============================

This software is a simplified simulator for illustrating the reaction of supply chain. It was implemented with the following aspects in mind:
 
- Input of sales for current month
- Input sales demand (in a 6 month planning window)
- Influence of sales demand on production supply (after a lead time of 3 months)
- Illustrate build-up stock excess
	- use also the future sales demand instead of sales to project the stock excess into the future
- Illustrate the bias (over multiple SKUs)
- Illustrate the forecast accuracy (over multiple SKUs)
- Ability to advance the model (and thus also the plots) in 1-month-long time units

See it in action [here](http://rawgit.com/altermarkive/Supply-Chain-Reaction-Simulator/master/simulation.html).
