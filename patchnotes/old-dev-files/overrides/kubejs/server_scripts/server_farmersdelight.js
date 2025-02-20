ServerEvents.recipes(event => {
	event.remove({output: 'farmersdelight:sweet_berry_cookie' })
	event.shaped(
				Item.of('farmersdelight:sweet_berry_cookie', 8),
				[
					'   ',
					'ABA',
					'   '
				],
				{
					A: 'minecraft:wheat',
					B: 'minecraft:sweet_berries'
				}
			).stage('test_stage')
})