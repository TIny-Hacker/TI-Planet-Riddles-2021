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

palettes = (
  (
    (247,176,36),(247,207,73),(231,89,0),(247,131,8),
  ),
)
images = (
  (
    b"\b\x05\n?\n\x05\x18\x05\n7\n\x05\x20\x05\n/\n\x05(\x05\n'\n\x050\x05\n\x1f\n\x058\x05\n\x17\n\x05@\x05\n\x0f\n\x05H\x05\n\a\n\x05P\x05\x16\x05X\x05\x0e\x05`\x05\x06\x05d\a\x06\a`\a\x02\x04\x02\aX\a\x02\x0c\x02\aP\a\x02\x04\a\x04\x02\aH\a\x02\x04"
    b"\x0f\x04\x02\a@\a\x02\x04\x17\x04\x02\a8\a\x02\x04\x1f\x04\x02\a0\a\x02\x04'\x04\x02\a(\a\x02\x04/\x04\x02\a\x20\a\x02\x047\x04\x02\a\x18\a\x02\x04?\x04\x02\a\x10\a\x02\x04G\x04\x02\a\b\a\x02\x04O\x04\x02\a\x00\a\x02\x04W\x04\x02\x0b\x02\x04_\x04"
    b"\x02\x03\x02\x04g\x04\x0eg\n\x01\n_\n\t\nW\n\x05\x00\x05\nO\n\x05\b\x05\nG\n\x05\x04"
  ),
)
draw_image(images[0], 0, 0, 32, palettes[0])
show()
wait()