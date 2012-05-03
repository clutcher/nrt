#Some key imports.
#Struct is used to create the actual bytes.
#It is super handy for this type of thing.
import struct, random

#Function to write a bmp file.  It takes a dictionary (d) of
#header values and the pixel data (bytes) and writes them
#to a file.  This function is called at the bottom of the code.
def bmp_write(d,the_bytes):
    mn1 = struct.pack('<B',d['mn1'])
    mn2 = struct.pack('<B',d['mn2'])
    filesize = struct.pack('<L',d['filesize'])
    undef1 = struct.pack('<H',d['undef1'])
    undef2 = struct.pack('<H',d['undef2'])
    offset = struct.pack('<L',d['offset'])
    headerlength = struct.pack('<L',d['headerlength'])
    width = struct.pack('<L',d['width'])
    height = struct.pack('<L',d['height'])
    colorplanes = struct.pack('<H',d['colorplanes'])
    colordepth = struct.pack('<H',d['colordepth'])
    compression = struct.pack('<L',d['compression'])
    imagesize = struct.pack('<L',d['imagesize'])
    res_hor = struct.pack('<L',d['res_hor'])
    res_vert = struct.pack('<L',d['res_vert'])
    palette = struct.pack('<L',d['palette'])
    importantcolors = struct.pack('<L',d['importantcolors'])
    #create the outfile
    outfile = open('Graphics/adj.bmp','wb')
    #write the header + the_bytes
    outfile.write(mn1+mn2+filesize+undef1+undef2+offset+headerlength+width+height+\
                  colorplanes+colordepth+compression+imagesize+res_hor+res_vert+\
                  palette+importantcolors+the_bytes)
    outfile.close()


def write_image_from_matrix(adjacencyMatrix):
    #Here is a minimal dictionary with header values.
    #Of importance is the offset, headerlength, width,
    #height and colordepth.
    #Edit the width and height to your liking.
    #These header values are described in the bmp format spec.
    #You can find it on the internet. This is for a Windows
    #Version 3 DIB header.
    weightHeight = len(adjacencyMatrix)
    d = {
        'mn1':66,
        'mn2':77,
        'filesize':0,
        'undef1':0,
        'undef2':0,
        'offset':54,
        'headerlength':40,
        'width':weightHeight,
        'height':weightHeight,
        'colorplanes':0,
        'colordepth':24,
        'compression':0,
        'imagesize':0,
        'res_hor':0,
        'res_vert':0,
        'palette':0,
        'importantcolors':0
        }

    #Build the byte array.  This code takes the height
    #and width values from the dictionary above and
    #generates the pixels row by row.  The row_mod and padding
    #stuff is necessary to ensure that the byte count for each
    #row is divisible by 4.  This is part of the specification.
    the_bytes = ''
    for row in range(d['height']-1,-1,-1):# (BMPs are L to R from the bottom L row)
        for column in range(d['width']):
            if adjacencyMatrix.item((row, column)) > 0:
                r = 0
                g = 0
                b = 0
            else:
                r = 250
                g = 250
                b = 250
            pixel = struct.pack('<BBB',b,g,r)
            the_bytes = the_bytes + pixel
        row_mod = (d['width']*d['colordepth']/8) % 4
        if row_mod == 0:
            padding = 0
        else:
            padding = (4 - row_mod)
        padbytes = ''
        for i in range(padding):
            x = struct.pack('<B',0)
            padbytes = padbytes + x
        the_bytes = the_bytes + padbytes

    #call the bmp_write function with the
    #dictionary of header values and the
    #bytes created above.
    bmp_write(d,the_bytes)
