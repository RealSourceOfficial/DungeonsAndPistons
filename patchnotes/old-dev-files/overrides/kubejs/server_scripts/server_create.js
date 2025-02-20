ServerEvents.recipes(event => {
  event.remove({ output: 'createaddition:electric_motor' })
	event.remove({ output: 'createaddition:alternator' })
	event.remove({ output: 'createaddition:connector' })
	event.remove({ output: 'createaddition:small_light_connector' })
	event.remove({ output: 'createaddition:large_connector' })
	event.remove({ output: 'createaddition:tesla_coil' })
})