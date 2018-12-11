from PIL import Image, ImageDraw, ImageFont

def render():
    img = Image.new('RGB', (1280, 720), color='white')
    fnt = ImageFont.truetype('assets/open-sans.ttf', 18)
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Hello how is it going?', fill='black', font=fnt)
    
    img.save('assets/result.png')

def render_kavanaugh(pos, ):
