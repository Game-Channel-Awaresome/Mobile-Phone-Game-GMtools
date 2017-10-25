#coding=utf-8

from django.conf import settings
from django.http import HttpResponse

from PIL import Image, ImageDraw, ImageFont
import cStringIO, string, os, random

def captcha(request):
    '''Captcha'''
    image = Image.new('RGB', (147, 49), color = (255, 255, 255))
    font_file = os.path.join(settings.BASE_DIR, 'static/fonts/arial.ttf')
    font = ImageFont.truetype(font_file, 47)
    draw = ImageDraw.Draw(image)
    randstr = ''.join(random.sample(string.letters + string.digits, 4))
    draw.text((7, 0), randstr, fill=(0, 0, 0), font=font)
    del draw
    request.session['captcha'] = randstr.lower()
    buf = cStringIO.StringIO()
    image.save(buf, 'jpeg')
    return HttpResponse(buf.getvalue(), 'image/jpeg')



