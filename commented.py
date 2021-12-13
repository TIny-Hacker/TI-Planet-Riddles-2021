from math import ceil

def nop(*argv): pass
show, wait = nop, nop
neg_fill_rect = False
has_color = True

try: # NumWorks, NumWorks + KhiCAS, TI-Nspire CX + KhiCAS
  import kandinsky
  fill_rect = kandinsky.fill_rect
  screen_w, screen_h = 320, 222
  neg_fill_rect = True
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
draw_image(images[0], 0, 0, 32, palettes[0], 1, 1, 5)       #Draws a small piece of the banner
show()
wait()