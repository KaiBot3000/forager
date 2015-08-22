####### big update to db (needs to be run in server.py)

@app.route('/describe')
def describe():
	'''Inputs dictionary of names and descriptions into db.'''

	plants = {
		'Anna apple': 'A very early season Golden Delicious style apple variety from Israel, noted for its very low chill requirement of less than 300 hours.',
		'Apple': 'Apple fruit features oval or pear shape. Its outer peel comes in different hues and colors depending upon the cultivar type. Internally, its crispy, juicy pulp is off-white to cream in color, and has a mix of mild sweet and tart flavor. Its seeds are bitter in taste, and therefore, inedible.',
		'Avocado': 'The avocado is a tree native to Mexico and Central America, classified in the flowering plant family Lauraceae along with cinnamon, camphor and bay laurel',
		'Bartlett pear': 'The fruit has a bell shape, considered the traditional pear shape in the west, and its green skin turns yellow upon later ripening, although red-skinned derivative varieties exist. It is considered a summer pear, not as tolerant of cold as some varieties. It is often eaten raw, but holds its shape well when baked, and is a common choice for canned or other processed pear uses.',
		'Beaked hazelnut': 'The beaked hazel nuts are tasty, but, they are quite small.',
		'Bearss lime': 'It has a uniquely fragrant, spicy aroma. The fruit is about 6 centimetres (2.4 in) in diameter, often with slightly nippled ends, and is usually sold while green, although it yellows as it reaches full ripeness.',
		'Beverly Hills apple': 'Fruit is similar to Macintosh.',
		'Bing cherry': 'Bing is a perfect cherry for use in baking and preserves.',
		'Black Mission fig': 'The matured Black Mission fig "fruit" has a tough peel (in this case, green giving way to deep purple), often cracking near the stem end upon ripeness, and exposing the pulp beneath. The soft creamy white interior contains a seed mass bound with jelly-like flesh. The edible seeds are numerous and generally hollow, unless pollinated.',
		'Brown Turkey fig': 'A classic, all-purpose fig.',
		'California walnut': ' Nuts are small but edible.',
		'Callaway Apple': 'The red fruit has yellow flesh that is crisp and mildly tart. Great for eating and jellies. Excellent food source for birds.',
		'Carob': 'These healthy pods also can be eaten raw, fresh off of the tree. When fresh and moist, the pods are chewy and sweet.',
		'Chinese hackberry': 'Leaves and bark are used in Korean medicine.',
		'Citrus': 'Includes a variety of fruits from oranges to limes.',
		'Clementine': 'The exterior is a deep orange colour with a smooth, glossy appearance.',
		'Common fig': 'Figs can be eaten fresh or dried, and used in jam-making.',
		'Common pear': 'Most varieties show little color change as they ripen. Because pears ripen from the inside out, the best way to judge ripeness is to "Check the Neck": apply gentle thumb pressure to the neck or stem end of the pear. If it yields to gentle pressure, then the pear is ripe, sweet, and juicy. ',
		'Common plum': 'The taste of the plum fruit ranges from sweet to tart; the skin itself may be particularly tart. It is juicy and can be eaten fresh or used in jam-making or other recipes.',
		'Date palm': 'Dry or soft dates are eaten out-of-hand, or may be pitted and stuffed with fillings such as almonds, walnuts, pecans, candied orange and lemon peel, tahini, marzipan or cream cheese. ',
		'European hackberry': 'The berries have been used to treat abnormal menstrual flow, colic, peptic ulcers, diarrhea and dysentery as well as being used as a pain killer.  A decoction made from the bark was used by certain Native American tribes to treat sore throats and venereal diseases.',
		'Flowering crab apple': 'Fruit varies in size and color, from 1/4 inch to 2 inches and from yellow and orange to purple to brilliant red.',
		'Fuji apple': 'Its main characteristic is the lovely pink speckled flush over a yellow-green background. It is also crisp and juicy, with dull white flesh which snaps cleanly. The flavor is predominantly sweet, very refreshing (especially if slightly chilled), but not particularly outstanding.',
		'Gala apple': 'Mildly sweet and vanilla-like with a floral aroma.',
		'Gordon apple': 'This variety bears medium to large, globe-shaped fruit with green, striped skin blushed red. The flesh is crisp, firm and white.',
		'Grapefruit': 'The grapefruit is a subtropical citrus tree known for its sour to semi-sweet fruit. ',
		'Gravenstein apple': 'The Gravenstein apple has a tart flavor. It is picked in July and August and is heavily used as a cooking apple, especially for apple sauce and apple cider. ',
		'Green gage plum': 'Greengage fruit are identified by their round-oval shape and smooth-textured, pale green flesh; they are on average smaller than round plums but larger than mirabelle plums (usually between 2 and 4 cm diameter). ',
		'Hinds black walnut': 'The nut has a smooth, brown, thick shell, that contains a small edible nutmeat.',
		'Hollyleaf cherry': 'Hollyleaf cherry fruits are dark red to bluish black, between one-half to 1 inch in diameter. The flesh is sweet and juicy. This tasty native cherry would be more commercially viable if it were not for the large pit in the center surrounded by a thin layer of fruit.',
		'Improved Meyer lemon': 'Fragrant flowers produce thin skinned, juicy lemons year round.',
		'Jelly palm': 'Ripe fruit are about the size of large cherry, and yellowish/orange in color, but can also include a blush towards the tip. The taste is a mixture of pineapple, apricot, and vanilla. ',
		'Lemon': 'The lemon fruit is an ellipsoid berry surrounded by a green rind, which ripens to yellow, protecting soft yellow segmented pulp. ',
		'Lisbon lemon': 'Fruit medium in size, elliptical to oblong; base tapering to inconspicuous neck; apex tapering likewise into a usually large, prominent nipple surrounded by an irregular areolar furrow, commonly deeper on one side.  Seed content variable, but usually few to none.  Color yellow at maturity.',
		'Loquat': 'The succulent, tangy flesh is white, yellow or orange and sweet to subacid or acid, depending on the cultivar.',
		'Marina arbutus': 'The fruit is edible but has minimal flavour and is not widely eaten. Fruit is good for fermentation.',
		'Northern hackberry': 'It produces small berries that turn orange-red to dark purple in the autumn',
		'Olive': 'The raw olives are very bitter. They are "cured" mostly by bacterial fermentation. Later they may be alternately washed with water and packed with salt. The procedures vary a lot, and different varieties of olives get different treatment.',
		'Oro Blanco grapefruit': 'A sweet seedless citrus hybrid fruit similar to grapefruit.',
		'Owari Satsuma': ' Seedless, medium sized orange fruit is sweet and juicy. Ripens early and stores very well.',
		'Persian lime': 'It has a uniquely fragrant, spicy aroma. The fruit is about 6 centimetres (2.4 in) in diameter, often with slightly nippled ends, and is usually sold while green, although it yellows as it reaches full ripeness.',
		'Pineapple guava': 'The fruit has a greyish-green skin and amber-colored flesh. The flavor is strong and tart with slight pineapple and papaya undertones. The texture is gritty and is similar to a pear with tiny edible seeds. The fruit is ready to eat when slightly soft and when the jellied sections of the fruit are clear. ',
		'Stewart avocado': 'The tree grows about 30 feet tall, and has small, dark purple fruits that ripen in late fall.',
		'Strawberry tree': 'The fruit is sweet when reddish, and tastes similar to a fig.',
		'Sweet almond': 'Fresh almond tastes completely different from the dried almond that we know and love. Fresh almonds, i.e. those that are still encased within a hard-fleshed, green shell, taste very creamy and milky. They have a less intense aroma than do dried almonds',
		'Walnut': 'Walnuts are part of the tree nut family. This food family includes Brazil nuts, cashews, hazelnuts (filberts), macadamia nuts, pecans, pine nuts, pistachios and walnuts.',
		'White mulberry': 'White mulberry fruits are generally very sweet but often lacking in needed tartness. ',
		'Winter Banana apple': 'They are pale yellow with faint pink blush. The flavor is a nice combination of sweet and tart, with a definite banana aroma and very dense & crisp texture.'
	}

	plant_objects = Plant.query.filter(Plant.plant_name.in_(plants)).all()

	for plant in plant_objects:
		plant.plant_description = plants[plant.plant_name]
	db.session.commit()

	return redirect(url_for('search', plant='all'))


@app.route('/categorize')
def categorize():
	'''Changes categories of trees imported from fuf.'''


	fruit = ['Anna apple', 'Avocado', 'Bartlett pear', 'Bearss lime', 
			'Beverly Hills apple', 'Bing cherry', 'Black Mission fig', 'Brown Turkey fig', 'Callaway Apple', 'Citrus'
			 'Clementine', 'Common fig', 'Common pear', 'Common plum', 'Date palm', 'Flowering crab apple', 
			 'Fuji apple', 'Gala apple', 'Gordon apple', 'Grapefruit', 'Gravenstein apple', 'Green gage plum',
			  'Hollyleaf cherry', 'Improved Meyer lemon', 'Jelly palm', 'Lemon', 'Lisbon lemon', 'Loquat', 
			  'Marina arbutus', 'Olive', 'Oro Blanco grapefruit', 'Owari Satsuma', 'Persian lime', 
			  'Pineapple guava', 'Stewart avocado', 'Strawberry tree']

	nut = ['Beaked hazelnut', 'California walnut', 'Hinds black walnut', 'Sweet almond', 'Walnut', 
			'White mulberry', 'Winter Banana apple']
	herb = ['Carob', 'Chinese hackberry', 'European hackberry', 'Northern hackberry']


	vegetable = []
	
	plant_objects = Plant.query.all()

	for plant in plant_objects:
		if plant.plant_name in fruit:
			plant.plant_category = 'fruit'
		elif plant.plant_name in nut:
			plant.plant_category = 'nut'
		elif plant.plant_name in herb:
			plant.plant_category = 'herb'
		else:
			print plan.plant_name

	print 'Done categorizing!'

	db.session.commit()

	return redirect(url_for('search', plant='all'))










