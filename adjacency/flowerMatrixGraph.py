from PIL import Image, ImageDraw

size = 4

im = Image.new('RGBA', (150 * size + 10, 150 * size + 10), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)

# Border
draw.line((0, 10 * 0 * size, 150 * size, 10 * 0 * size), fill='#000000', width=2)
draw.line((0, 10 * 15 * size, 150 * size, 10 * 15 * size), fill='#000000', width=2)
draw.line((10 * 0 * size, 0, 10 * 0 * size, 150 * size), fill='#000000', width=2)
draw.line((10 * 15 * size, 0, 10 * 15 * size, 150 * size), fill='#000000', width=2)

# Lattice
for i in xrange(16):
    draw.line((0, 10 * i * size, 150 * size, 10 * i * size), fill='#000000')
for i in xrange(16):
    draw.line((10 * i * size, 0, 10 * i * size, 150 * size), fill='#000000')

# Grand small
draw.line((0, 10 * 3 * size, 10 * 6 * size, 10 * 3 * size), fill='#000000', width=2)
draw.line((10 * 3 * size, 0, 10 * 3 * size, 10 * 6 * size), fill='#000000', width=2)

#Grand big
draw.line((0, 10 * 6 * size, 150 * size, 10 * 6 * size), fill='#000000', width=2)
draw.line((10 * 6 * size, 0, 10 * 6 * size, 150 * size), fill='#000000', width=2)

#Right corner small blank
draw.rectangle([10 * 3 * size + 2, 10 * 3 * size + 1, 10 * 6 * size - 1, 10 * 6 * size - 2], fill='#FFFFFF')

#Right corner big blank
draw.rectangle([10 * 6 * size + 2, 10 * 6 * size + 1, 150 * size - 1, 150 * size - 2], fill='#FFFFFF')

#Center grand
draw.line([10 * 3 * size, 10 * 3 * size, 10 * 3 * size, 10 * 9 * size], fill='#000000', width=2)
draw.line([10 * 3 * size, 10 * 3 * size, 10 * 9 * size, 10 * 3 * size], fill='#000000', width=2)
draw.line([10 * 9 * size, 10 * 3 * size, 10 * 9 * size, 10 * 9 * size], fill='#000000', width=2)
draw.line([10 * 3 * size, 10 * 9 * size, 10 * 9 * size, 10 * 9 * size], fill='#000000', width=2)

# im.show()
im.save('first.png')

#Clear image
draw.rectangle([0, 0, 150 * size +10, 150 * size +10], fill='#FFFFFF')

# Border
draw.line((0, 10 * 0 * size, 150 * size, 10 * 0 * size), fill='#000000', width=2)
draw.line((0, 10 * 15 * size, 150 * size, 10 * 15 * size), fill='#000000', width=2)
draw.line((10 * 0 * size, 0, 10 * 0 * size, 150 * size), fill='#000000', width=2)
draw.line((10 * 15 * size, 0, 10 * 15 * size, 150 * size), fill='#000000', width=2)

# Grand small
draw.line((0, 10 * 3 * size, 10 * 6 * size, 10 * 3 * size), fill='#000000', width=2)
draw.line((10 * 3 * size, 0, 10 * 3 * size, 10 * 6 * size), fill='#000000', width=2)

#Grand big
draw.line((0, 10 * 6 * size, 150 * size, 10 * 6 * size), fill='#000000', width=2)
draw.line((10 * 6 * size, 0, 10 * 6 * size, 150 * size), fill='#000000', width=2)

#Center grand
draw.line([10 * 3 * size, 10 * 3 * size, 10 * 3 * size, 10 * 9 * size], fill='#000000', width=2)
draw.line([10 * 3 * size, 10 * 3 * size, 10 * 9 * size, 10 * 3 * size], fill='#000000', width=2)
draw.line([10 * 9 * size, 10 * 3 * size, 10 * 9 * size, 10 * 9 * size], fill='#000000', width=2)
draw.line([10 * 3 * size, 10 * 9 * size, 10 * 9 * size, 10 * 9 * size], fill='#000000', width=2)

#Center grand small
draw.line([10 * 2 * size, 10 * 2 * size, 10 * 2 * size, 10 * 4 * size], fill='#000000', width=2)
draw.line([10 * 2 * size, 10 * 2 * size, 10 * 4 * size, 10 * 2 * size], fill='#000000', width=2)
draw.line([10 * 4 * size, 10 * 2 * size, 10 * 4 * size, 10 * 4 * size], fill='#000000', width=2)
draw.line([10 * 2 * size, 10 * 4 * size, 10 * 4 * size, 10 * 4 * size], fill='#000000', width=2)

im.save('second.png')

#Right exceptive
draw.line([10 * 4 * size, 10 * 11 * size, 10 * 6 * size, 10 * 11 * size], fill='#000000', width=2)
draw.line([10 * 4 * size, 10 * 11 * size, 10 * 4 * size, 10 * 15 * size], fill='#000000', width=2)
#Right exceptive symetric
draw.line([10 * 11 * size, 10 * 4 * size, 10 * 11 * size, 10 * 6 * size], fill='#000000', width=2)
draw.line([10 * 11 * size, 10 * 4 * size, 10 * 15 * size, 10 * 4 * size], fill='#000000', width=2)

im.save('third.png')