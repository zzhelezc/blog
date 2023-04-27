#!/usr/bin/env python3

from photo_data import *
import sys

def gen_page_html(title, group_id, images):
    
    images_body = ''
    
    for i in images:
        img_title = titles.get('.' + i, '')
        item = (
            f'<div class="{group_id}"\n'
            f'href="{i}"\n'
            f'title="{img_title}"></div>\n\n'
        )
        images_body += item 
    
    page = (
        '---\n'
        'layout: page\n'
        f'title: {title}\n'
        '---\n\n'

        '<!DOCTYPE html>\n'
        '<html>\n'
        '<head>\n'
        '<link rel="stylesheet" href="/public/css/font.css" />\n'
        '<meta charset=\'utf-8\'/>\n'
        '<link rel="stylesheet" href="/public/css/colorbox.css" />\n'
        '<script src="/public/js/jquery.js"></script>\n'
        '<script src="/public/js/jquery.colorbox-min.js"></script>\n'
        '<script>\n'
        '$(document).ready(function(){\n'
        '    $(".' + group_id +'").colorbox({rel:\'' + group_id + '\', transition:"none", maxHeight: "95%",\n'
        '                           maxWidth: "95%",\n'
        '                           open: true, opacity: 1, overlayClose: true,\n'
        '                           onClosed:function(){ document.location.href ='
        '                           "https://wandering-nonsense.com"; }\n'
        '                           });\n'
        '});\n'
        '\n'
        '</script>\n'
        '</head>\n\n'
        '<body>\n'
        f'{images_body}'
        '</body>\n'
        '</html>\n')

    return page



def gen_page(album, group_id):
    d = album
    items = photos[d]

    images = []

    for i in items:
        
        if isinstance(i, tuple):
            a = i[0]
            b = i[1]

            a1 = a.replace('.jpg', '')
            b1 = b.replace('.jpg', '')
            
            cmd = f'montage "./photos/{d}/{a}" "./photos/{d}/{b}" -tile 2x1 -geometry +40+0 "./photos/{d}/{a1}-{b1}.jpg"'
                
            os.system(cmd)
            images.append(f'/photos/{d}/{a1}-{b1}.jpg')

        else:
             images.append(f'/photos/{d}/{i}')
             

    
    page = gen_page_html(d, f'gen_group{group_id}', images)

    filename = d.lower().replace(' ', '_').replace(':', '_') + '.html'
    with open(filename, 'w') as f:
        f.write(page)


def main():
    dirs = list(photos.keys())
    
    for i, d in enumerate(dirs):
        print(f'generating html page for {d}...')
        gen_page(d, i)
        
    print('done.')    
            
        

if __name__ == '__main__':
    main()
