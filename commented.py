from math import ceil

platform = ''                     #Some interesting stuff has been added up here on day 12. 
try: from sys import platform    #No clue what it does
except: pass                     #This stuff got commented out on day 14. Now it's un-commented again on day 17. And now it's commented again the 25th. Uncommented the 27th.

def nop(*argv): pass
show, wait = nop, nop
neg_fill_rect = False
has_color = True

try: # NumWorks, NumWorks + KhiCAS, TI-Nspire CX + KhiCAS
  import kandinsky
  fill_rect = kandinsky.fill_rect
  screen_w, screen_h = 320, 222
  neg_fill_rect = platform!='nspire' and platform!='numworks'       #Not sure what this does but it was also added day 12. 
except:
  try: # TI
    import ti_draw
    try: # TI-Nspire CX II
      ti_draw.use_buffer()
      show = ti_draw.paint_buffer
    except: # TI-83PCE/84+CE Python
      wait = ti_draw.show_draw
    screen_w, screen_h = ti_draw.get_screen_dim()
    try: # check TI-83PCE/84+CE ti_draw 1.0 fill_rect bug
      ti_draw.fill_rect(0,0,1,1)
      def fill_rect(x, y, w, h, c):
        ti_draw.set_color(c[0], c[1], c[2])
        ti_draw.fill_rect(x, y, w, h)
    except: # workaround
      def fill_rect(x, y, w, h, c):
        ti_draw.set_color(c[0], c[1], c[2])
        ti_draw.fill_rect(x - 1, y - 1, w + 2, h + 2)
  except:
    try: # Casio Graph 90/35+E II, fx-9750/9860GIII, fx-CG50
      import casioplot
      casioplot.set_pixel(0, 0, (0, 0, 255))
      col = casioplot.get_pixel(0, 0)
      has_color = col[0] != col[2]
      screen_w, screen_h = has_color and (384, 192) or (128, 64)
      show = casioplot.show_screen
      def fill_rect(x, y, w, h, c):
        for dy in range(h):
          for dx in range(w):
            casioplot.set_pixel(x + dx, y + dy, c)
    except:
      try: # HP Prime
        import hpprime
        screen_w, screen_h = hpprime.grobw(0), hpprime.grobh(0)
        hpprime.dimgrob(1, screen_w, screen_h, 0)
        def col3_2_rgb(c, bits=(8,8,8), bgr=1):
          return c[2*bgr]//2**(8 - bits[0]) + c[1]//2**(8 - bits[1])*2**bits[0] + c[2*(not(bgr))]//2**(8-bits[2])*2**(bits[0] + bits[1])
        def fill_rect(x, y, w, h, c):
          hpprime.fillrect(1, x, y, w, h, col3_2_rgb(c), col3_2_rgb(c))
        def show():
          hpprime.strblit(0, 0, 0, screen_w, screen_h, 1)
        def wait():
          while hpprime.keyboard(): pass
          while not(hpprime.keyboard()): pass
      except:
        pass
if not neg_fill_rect:
  _fill_rect = fill_rect
  def fill_rect(x, y, w, h, c):
    if w < 0:
      x += w
      w = -w
    if h < 0:
      y += h
      h = -h
    _fill_rect(x, y, w, h, c)

def draw_image(rle, x0, y0, w, pal, zoomx=1, zoomy=1, itransp=-1):
  if not has_color:
    pal = list(pal)
    g_min, g_max = 255, 0
    for k in range(len(pal)):
      c = pal[k]
      g = 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
      g_min = min(g_min, g)
      g_max = max(g_max, g)
      pal[k] = g
    for k in range(len(pal)):
      pal[k] = pal[k]<(g_min + g_max) / 2 and (0,0,0) or (255,255,255)
  i, x = 0, 0
  x0, y0 = int(x0), int(y0)
  nvals = len(pal)
  nbits = 0
  nvals -= 1
  while(nvals):
    nvals >>= 1
    nbits += 1
  maskval = (1 << nbits) - 1
  maskcnt = (0xFF >> nbits >> 1) << nbits
  while i<len(rle):
    v = rle[i]
    mv = v & maskval
    c = (v & maskcnt) >> nbits
    if (v & 0b10000000 or nbits == 8):
      i += 1
      c |= rle[i] << (7 - nbits + (nbits == 8))
    c = (c + 1)
    while c:
      cw = min(c, w - x)
      if mv != itransp:
        fill_rect(x0 + x*zoomx, y0, cw*zoomx, zoomy, pal[mv])
      c -= cw
      x = (x + cw) % w
      y0 += x == 0 and zoomy
    i += 1

#Background tile

palettes = (
  (
    (247,176,36),(247,207,73),(231,89,0),(247,131,8),
  ),
)
images = (      #Background tile images, split because lines on the casio models may only have 256 characters
  (
    b"\b\x05\n?\n\x05\x18\x05\n7\n\x05\x20\x05\n/\n\x05(\x05\n'\n\x050\x05\n\x1f\n\x058\x05\n\x17\n\x05@\x05\n\x0f\n\x05H\x05\n\a\n\x05P\x05\x16\x05X\x05\x0e\x05`\x05\x06\x05d\a\x06\a`\a\x02\x04\x02\aX\a\x02\x0c\x02\aP\a\x02\x04\a\x04\x02\aH\a\x02\x04"
    b"\x0f\x04\x02\a@\a\x02\x04\x17\x04\x02\a8\a\x02\x04\x1f\x04\x02\a0\a\x02\x04'\x04\x02\a(\a\x02\x04/\x04\x02\a\x20\a\x02\x047\x04\x02\a\x18\a\x02\x04?\x04\x02\a\x10\a\x02\x04G\x04\x02\a\b\a\x02\x04O\x04\x02\a\x00\a\x02\x04W\x04\x02\x0b\x02\x04_\x04"
    b"\x02\x03\x02\x04g\x04\x0eg\n\x01\n_\n\t\nW\n\x05\x00\x05\nO\n\x05\b\x05\nG\n\x05\x04"
  ),
)
for y in range(ceil(screen_h / 32)):      #Fill background with tiles (Tiles are 32x32)
  for x in range(ceil(screen_w / 32)):
    draw_image(images[0], x*32, y*32, 32, palettes[0])
show()

#Draw the floor

palettes = (
  (
    (7,97,182),(55,139,223),(99,176,247),(141,216,247),
  ),
)
images = (      #Small blue floor tile
  (
    b"\x80\x01!\x14!\x18\x1e\x19\x1e\x19\x06\x17\x1a\x1f\x1a\x1f\x1a\x1f\x1a\x17\x06\x19\x1e\x19\x1e\x18!\x14!\x80\x01"
  ),
)
for x in range(ceil(screen_w / 16)):      #Draws the entire floor using a loop
  draw_image(images[0], x*16, screen_h-16, 16, palettes[0])
show()

#Begin the banner at the top

palettes = (
  (
    (239,89,107),(247,207,81),(0,0,0),(182,26,36),(239,97,0),(0,0,0),
  ),
)
images = (      #Piece of the red banner with stars on it. The characters of the image did not provide any hidden links, at least not to me.
  (
    b"\xc0\x011\xc0\x01\x02)\xc0\x01\x03\x02!\xc0\x01\x0b\x02!\xc0\x01\x0b!\xc8\x011\xc0\x011\xb8\x01!\x021\x90\x01\x11\n\x03)\x02\x88\x01\t\n\x13!\x02\x03\x88\x01\n#\x19\x02\x0b\x88\x01+\x00\x19\x0b\x90\x01\x1b\x10!\x98\x01\x0b\x20!\xd0\x01\x02!\xc8\x01"
    b"\x03\n\x11\xc8\x01\x13\n\t\xc0\x01#\n\xe8\x01\x0b\xb8\x02\tX\x13p\t@+h\x19\x18Kh\x19[Pi#\x18C\x02Y\x02\x0b0K\x02I\x02\x03@S\x029\x02\x03(\xfb\x009\x03\x20\x1b\b3\x18I\x18\x13pI\b\x1b\x18\x03H!\n!\x1b\x18\x0bH\x11\n\x0b\n\x11\x13\x20\x03\x04@\t\n+\n"
    b"\t\x03\x20\x0b\x04@\nK\n(\x0b\x04@c(\x13\x04\x018[0\x0b\x0c\x01(c0\x13\x0c\t\x83\x010\x1b\x0c\ts@\x13\x141;H\x1b\x14)\x02+P\x1b\x1c!\x02\x1b`#\x1c\x19\x02\x0bp#\x1c\x05\x19\x80\x01+\x14\r!p+\x1c\r!h+\x1c\x15\x02!X+$\x15\x03\n\x11P+$\x1d\x13\n\t83,"
    b"\x1d#\n(;,%\x00+\x10K,-\x10\xfb\x00,5\x8b\x01,=\xfb\x004Ek<M[DUCT]#dm\xfc\x00\xfd\x00\x01d\x8d\x01\tL\x9d\x01\x04\t,\xb5\x01\x0c\t\x14\xc5\x01"
  ),
)
for x in range(ceil(screen_w / 64)):      #Draw the banner across the stage
  draw_image(images[0], x*64, 0, 32, palettes[0], 1, 1, 5)          #First the non-reversed tile
  draw_image(images[0], (x+1)*64, 0, 32, palettes[0], -1, 1, 5)     #Afterwards the reversed tile, at an offset from the original.
show()

#Mysterious functions of mystery

def draw_rect_z(x, y, w, h, c, z=1):     #The only time this mysterious function is used is in the equally mysterious `qr_mark()` function.  
  for dy in (0, h - 1):                  #I'm not 100% sure exactly what this function does, but judging by the name it might draw a rectangle.
    fill_rect(x, y + dy*z, w*z, z, c)    #I was an idiot. `z` is not for color like I thought, `c` is for color. 
  for dx in (0, w - 1):
    fill_rect(x + dx*z, y, z, h*z, c)

def qr_mark(x, y, s, c, z=1):                            #The comments above are old! Now we know what this function does.
  draw_rect_z(x, y, s, s, c, z)                          #It was first used day 15
  fill_rect(x + 2*z, y + 2*z, (s - 4)*z, (s - 4)*z, c)    

#The first door

palettes = (
  (
    (0,0,0),(247,172,107),(133,71,73),(157,114,18),(207,147,55),(247,247,247),      #Door palette
  ),
  (
    (0,0,0),(36,35,36),(198,0,18),(247,26,55),(157,0,0),(231,97,81),(239,147,90),(247,183,133),(55,114,167),(247,247,247),(72,155,207),(36,71,133),(166,80,0),(239,199,45),(223,131,45),      #Mario Palette
  ),
  (
    (0,0,0),(0,0,0),(255,183,45),(255,255,247),(255,216,141),     #Icon Palette for NumWorks. Maybe also other icons later. Looks like it might be for other things too.
  ),
  (
    (0,0,0),(0,0,0),(27,58,157),(157,172,215),(247,251,247),      #Two palettes were added day 14. Possibly the Casio icon.
  ),
  (
    (0,0,0),(223,41,45),                                          #TI Palette
  ),
)
images = (      #The door. As before, images are split into lines =< 256 characters.
  (
    b"\x80\x01a\x02\b\x01[\x02\b\x01\x03\x19\x0b\x19\x03\x02\b\x01\x03\x01\x0b\x01\x0b\x01\x0b\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03"
    b"\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x19\x0b\x19\x03\x02\b\x01[\x02\b\x05Y\x02\b\x01\\\x02\b\x01\r\x03\x14\x01$\x02\b\x01\r\x02\x0c\x01\x0c\x01\x14\x02\b\x01\x03\n\x04\x01\x0c\x01\x1c\x02\b"
    b"\x01\x13\x04\x0b\x04#\x02\bj\b\x01[\x02\b\x01\x03\x19\x0b\x19\x03\x02\b\x01\x03\x01\x0b\x01\x0b\x01\x0b\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01"
    b"\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x01\x0c\x01\x0b\x01\x0c\x01\x03\x02\b\x01\x03\x19\x0b\x19\x03\x02\b\x01[\x02\bj\x80\x01"
  ),
  (             #Mario. Split into lines for the requirements on Casio models.
    b"\xe0\n1\x90\x01\x11\x02#\x01\xf0\x00\x01\x04\"\x13\x01`\x01\x04\"Q0\x01$\x81\x01\x20\x01\x14\x11E\x11\x20A\x05\x16\x01\x06\x110\x01\x16\x11\x05\x16\x01\x06!\x20\x01\x16!\x056\x17\x01\x10\x01\x05\x06\x05\x01\x05\x06\x01\x15&\x01\x20\x01%\x061\x15!"
    b"\x20\x11\x15\x16A0\x11\b\x01E\x01@\x01\x04\x02\x01\bAP\x01\x12\x03!\x04\x03\x11\x00\x01\x10\x01\x04\x02\x03\x01&\x01\x04\x03\x11\x06\x01\x00\x01\x04\x02\x01\x05\x06\x17\x06\x01\x04\x02\x01\x05\x01\x00\x01\x14\x01\x15&A\x10\x11\x14\x01%\x01\t\x1a\t"
    b"\x01\x20!\x0b!\x19\x1a\t\x01\x20\x01+\x18\n\b*\b\x010\x01\x0b\x18\n\b\x0b8\x11\x10\x01\x0c\x01\x0b\x18\x0b\x01\x1b\b\x01\r\x0e\x01\x00\x01\x0c\x01+\x01\x00\x01\x0b\x01\r\x0e\x0c\x01\x00\x01\x0c\x0e!\x20\x01\x1e\x0c\x01\x20\x01\x0c\x1e\x0c\x01\x10"
    b"\x01\x1c\x01@A\x20\x11\x20"
  ),
  (             #NumWorks icon which appears above the center door. Also, it appears this might include something for Casio? I am a bit confused.
    b"\x80\x01i\x00\x01j\tj\t\x12\x03\x04\x1a\x04\x03\x12\t\x12\x0b\x04\x12\x04\x03\x12\t\x12\x13\x12\x04\x03\x12\t\x12\x03\x04\x0b\n\x04\x03\x12\t\x12\x03\x0c\x03\x04\x02\x04\x03\x12\t\x12\x03\x04\x02\x04\x03\x0c\x03\x12\t\x12\x03\x04\n\x0b\x04\x03\x12"
    b"\t\x12\x03\x04\x12\x13\x12\t\x12\x03\x04\x12\x04\x0b\x12\t\x12\x03\x04\x1a\x04\x03\x12\tj\tj\x01"
  ),
  (             #I'm pretty sure this is the Casio icon.
    b"\x80\x01i\x00\x01j\t\n\x0b,\x0b\n\t\x02\x03T\x02\t\x02\\\x03\t\x03\x14\x03\"\x14\x03\t\x03\x14J\t\x03\x14J\t\x03\x14J\t\x03\x14*\x14\x03\t\x02\x14+\x14\x03\t\x02\x03T\x03\t\n\x03D\x03\x02\t\x1a3\x12\tj\x01"
  ),
  (             #That would make this the TI icon.
    b"\x06\a\x16\a\x02\x03\x0e\a\x16\t\x00\x01\x00\x05\b\t\x00\x01\x00\x05\b\a\x00\x03\x02\x03\x00\r\x02\x03\x00\a\x00\r\x00\x01\x00\t\x02\x0b\x00\x01\x00\t\x02\x0b\x00\x01\x00\t\x04\x03\x00\x03\x06\x05\x0e\x01\x04\x03\x12\t\x16\a\x16\x05\x1a\x05\x06"
  ),
)
for j in range(-1, 2, 2):     #A similar method as before is used to draw Mario and the door, as well as the icons. However, this time it is done differently to allow for the other two doors.
  for i in range(1, 3):                             #This loop just draws mario, doors and icons.
    x = screen_w//2 - j*(screen_w * i // 6)
    if i+j != 3:
      qr_mark(x - 7, screen_h - 15, 7, [(k + 2) % 3 == i + j and 255 or 0 for k in range(3)], 2)        #This draws the different keys under their respective doors. 
      show()
      draw_image(images[2 + i + j], x - 8, screen_h - 64, 16, palettes[2 + i + j], itransp=0)             #Doors?
      show()
    draw_image(images[i+j == 3], x - 8, screen_h - 48, 16, palettes[i+j == 3], itransp= i+j!=3 and -1)    #Icons?
    show()

#Treasure Chest

palettes = (      #Palette for treasure chest
  (
    (0,0,0),(0,0,0),(190,232,247),(190,97,0),(231,139,18),(157,199,239),(247,247,247),(247,176,64),(149,54,0),(133,172,207),
  ),
)
images = (
  (               #Top of treasure chest
    b"Q\x061\x05\xc1\x02\x19\x01\t\x01\x16\x11\x02\x05\x01\t\x01\x19\x01\t\x01\x89\x01\x01\t\x11\x15\x01\x05\x01\x16\x11\x02\x05\x01\x05\x01\x15\x01\x05\x01\x85\x01\x01\x05\x11\x12!\x16\x11\x02\x05!\x12\x01\x05\xa1\x01\x05\x11\x12\x01\b\x01B\x05\x01\b\x01\x12"
    b"\x01\x05\x01\x88\x01\x01\x05\x11\x16\x01\x18Q\x18\x01\x16\x01\x05\x01\x88\x01\x01\x05\x11\x12\x01\b\x03h\x04\x01\x12\x01\x05\x01\x88\x01\x01\x05\x11\x16\x01\bc\x14\x01\x16\x01\x05\x01h\x03\b\x01\x05\x11\x16\x01\bS$\x01\x16\x01\x05\x01X\x13\b\x01\x05\x11"
    b"\x12\x01\bC$\x03\x01\x12\x01\x05\x01H#\b\x01\x05\x11\x16\x01\b3$\x13\x01\x16\x01\x05\x018#\x18\x01\x05\x11\x12\x01\x98\x01\x01\x12\x01\x05\x01\x88\x01\x01\x05\x11\x12\xb1\x01\x12\x01\x05\xa1\x01\x05\x11\x12\x01\x19\x05b\x01\x12\x01\x05\x01e\x19\x01\x05"
    b"\x11\x12\x01\x19\x05b\x01\x12\x01\x05\x01e\x19\x01\x05\x81\x04"
  ),
  (               #Bottom of treasure chest
    b"P\xb1\x02\x90\x01\x11\x12\x11\xf4\x00\x01\x12\x11%\x11`\x01\x16\x11\x04\xf7\x00\x01\x16\x01\x15!\x15\x01@\x01\x16\x01\x04\x87\x01\x01\x16\x01\x05\x11(\x11\x05\x010\x01\x16\x01\x04\x87\x01\x01\x16\x01\x05\x01H\x01\x05\x01\x20\x01\x16\x01\x03\x84\x01\x01"
    b"\x16\x01\x05\x01h\x01\x05\x01\x10\x01\x16\x01\x03\x84\x01\x01\x16\x01\x05\x01h\x01\x05\x01\x10\x01\x16\x01\x03\x84\x01\x01\x16\x01\x05\x01h\x01\x05\x01\x00\x01\x12\x01\b\x83\x01\x01\x12\x01\x05\x01h\x03\b\x01\x05\x11\x16\x01\b\x83\x01\x01\x16\x01\x05"
    b"\x01X\x13\b\x01\x05\x11\x16\x01\b\x83\x01\x01\x16\x01\x05\x01H#\b\x01\x05\x11\x12\x01\b\x83\x01\x01\x12\x01\x05\x018#\x18\x01\x05\x11\x16\x01\b\x03Q\b\x03\x01\x16\x01\x05\x01(#(\x01\x05\x11\x12\x01\b\x01&\x12\x05\x01\b\x01\x12\x01\x05\x01\x18#8\x01\x05"
    b"\x11\x12\x01\b\x01\x16\x11\x02\x05\x01\b\x01\x12\x01\x05\x01\b#(\x03\b\x01\x05\x11\x15\x01\b\x01\x061\x05\x01\b\x01\x15\x01\x05\x01\x88\x01\x01\x05\x01"
  ),
  (               #Opening treasure chest
    b"P\xc1\x02\x80\x01\x11\x12\x01\x03\x84\x01\x01\x12\x11%\x11P\x01\x16\x01\x14\x87\x01\x01\x16\x01\x15!\x15\x01@\x01\x16\x01\x04\x97\x01\x01\x16\x01\x05\x01(\x01\x05\x010\x01\x16\x01\x04\x97\x01\x01\x16\x01\x05\x01H\x01\x05\x01\x20\x01\x16\x01\x03\x94\x01"
    b"\x01\x16\x01\x05\x01H\x01\x05\x01\x20\x01\x12\x01\x03\x94\x01\x01\x12\x01\x05\x01H\x01\x05\x01\x20\xa1\x02\x05\x01X\x01\x05\x01\x20\x01\x89\x02\x11X\x01\x05\x010\x01\t\xe1\x01\t\x11H\x01\x05\x01@\x01\t\xe1\x01\t\x118\x01\x05\x01P\x01\t\xe1\x01\t\x11("
    b"\x01\x05\x01P\x91\x02\t\x11\x18\x01\x05\x01@\x01&\x12\x05\xc1\x01\t\x11\b\x01\x05\x01@\x01\x16\x11\x02\x05\xd1\x01\t!\x05\x01@\x01\x061\x05\xe1\x01\t\x11\x05\x01"
  ),
)
for i in range(2):                #Displays the treasure chest 
  draw_image(images[-i], screen_w//2-16, screen_h-32-16*i, 32, palettes[0], itransp=0)
show()

def qr_size(v):         #presumably the size of the QR Code
  return 17 + 4*v

#This bit is very confusing to me

qr_ver = 3        #Vertical
qr_margin = 4                       #Between inner and outer square
qr_size_code = qr_size(qr_ver)       #Size of QR code based on vertical height
qr_size_code_margin = qr_size_code + 2*qr_margin + 4    #Other margin?
qr_zoom = max(1, min(screen_w // qr_size_code_margin, (screen_h - 128) // qr_size_code_margin))   #QR zoom: Whether or not the code will be zoomed in
qr_size_code_margin -= 4            #Other margin on QR code adjusted?
qr_width = qr_size_code_margin * qr_zoom      #Width of QR Code
x_qr = (screen_w - qr_width) // 2       #X and Y of QR Code
y_qr = (screen_h - qr_width) // 2
for k in range(1, 3):
  draw_rect_z(x_qr - k*qr_zoom, y_qr - k*qr_zoom, qr_size_code_margin + 2*k, qr_size_code_margin + 2*k, k > 1 and (0, 0, 0) or (255, 255, 255), qr_zoom)    #Draws QR code?
qr_margin *= qr_zoom          #Margin around the border?
fill_rect(x_qr, y_qr, qr_width, qr_width, (0,64,64))        #Fills the background of the QR code

def qr_alignments(v):         #Not sure what this does. I think it's related to the tiny box
  s = qr_size(v)
  positions = []
  n = v // 7 + 2
  first = 4
  positions.append(first)
  last = s - 5 - first
  step = last - ((first + last*(n - 2) + (n - 1)//2) // (n - 1) & -2)
  second = last - (n - 2) * step
  positions.extend(range(second, last + 1, step))
  return position

#This draws the tiny QR code corner box thingy in the corners of the QR Code frame

def qr_frame(v, x, y, c, z=1):
  s = qr_size(v)
  l = (0, s - 7)
  for dy in l:                    #This loops draws the corner boxes
    for dx in l:
      if not dx or not dy:
        qr_mark(x + dx*z, y + dy*z, 7, c, z)
  for i in range(8, s-8, 2):                      #Begins to draw the QR Code in the box.
    fill_rect(x + i*z, y + 6*z, z, z, c)          #Draws top dots
    fill_rect(x + 6*z, y + i*z, z, z, c)          #Draws left dots
  l = qr_alignments(v)                            #This stuff is related to the tiny box in the corner
  for dy in l:
    for dx in l:
      if not (dy < 8 and (dx < 8  or dx > s - 10) or dx < 8 and dy > s - 10):
        qr_mark(x + (dx - 0)*z, y + (dy - 0)*z, 5, c, z)

qr_frame(qr_ver, x_qr + qr_margin, y_qr + qr_margin, (255,255,255), qr_zoom)      #Draws the tiny QR Code box in white

palettes = (                    #Palette for the QR Code
  (
    (0,0,0),(255,255,255),
  ),
  (                             #Same palette for the other part of the QR Code
    (0,0,0),(255,255,255),
  ),
)
images = (                      #Right half of the QR Code
  (
    b"\x1e\x01\x02\x03,\x05\x02\x012\x014\x014\x01\x00\x056\x01n\x030\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x20\a\x00\a\x04\x01\x1a\a\x02\x03\x02\x01\"\x01\x00\x01\x00\x05\x02\x01\x00\x01\x00\x01\x1c\x01\x00\x03\x0c\x03\x1e\x05\x02\x0b\x04\x01\x1c"
    b"\x01\n\x01\x00\x05&\x03\x00\x03\x00\x01\x02\x01$\x01\x00\x01\x02\x01\x00\x03\"\x01\x02\x0b\x00\x01\x00\x01\x1c\x03\x00\x01\x00\x01\x02\x03\x00\x01\"\x01\x00\x05\n\x01\x1c\x01\x00\x01\x00\x03\n\x05\x1c\x03\x0e\a\x1c\x01\x02\x03\b\x03$\x05\x0c\x032"
    b"\x05\x1c\x01\x00\x03\x00\x01\x06\x03\x20\x01\x00\a\x00\x0b\x1e\x03\x00\x01\x00\x01\x04\x03\x00\x01\x1e\x03\x00\x01\x02\x01\x00\a\x02"
  ),
  (                             #Left part of the QR Code
    b"\x16\x01\x00\x01*\x01\x04\x038\x01*\x01\x06\x01f\x01\n\x01n\x01\x1a\t\x02\x03\b\x01$\x01\x02\x01:\x01^\x01\x0c\x01(\x01<\x01\x00\x01\b\x01\"\x01\x0c\x01:\x01\x00\x01\x18\x01\x02\x01\x00\x01\x04\x01\x02\x01\x1e\x01\x14\x01\x1e\x016\x01\n\x018\x01"
    b"\x02\x01\x00\x01,\x03\x02\x016\x01.\x01\x06\x03*\x01\x06\x01,\x016\x016\x01\x00\x01\""
  ),
)

for k in range(len(images)):    #Drawing the QR Code
  draw_image(images[k], x_qr + qr_margin, y_qr + qr_margin, qr_size_code, palettes[k], zoomx=qr_zoom, zoomy=qr_zoom, itransp=0)

show()
wait()