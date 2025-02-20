ServerEvents.recipes(event => {
  event.remove({ output: 'solapplepie:lunchbag' })
	event.remove({ output: 'solapplepie:lunchbox' })
	event.remove({ output: 'solapplepie:golden_lunchbox' })
})