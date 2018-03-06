# encoding:utf-8
#!/usr/bin/python3
import zipfile
import os.path

'''
Script Name     : createEpubBook.py
Author          : svoid
Created         : 2015-03-28
Last Modified   : 
Version         : 1.0
Modifications   : 
Description     : 根据HTML生成epub文档
'''


def create_mimetype(epub):
    epub.writestr('mimetype', 'application/epub+zip',
                  compress_type=zipfile.ZIP_STORED)


def create_container(epub):
    container_info = '''
    
      
        
      
  
    '''
    epub.writestr('META-INF/container.xml', container_info,
                  compress_type=zipfile.ZIP_STORED)


def create_content(epub, path):
    content_info = '''
    
    
      
        Hello World: My First EPUB
        Svoid
        urn:uuid:12345
        
      
      
          %(manifest)s
        
        
        
      
      
          %(spine)s
        
        
      
      
        
      
    
    '''
    manifest = ''
    spine = ''
    for html in os.listdir(path):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            manifest += '{}'.format(basename)
            spine += '{}'.format(basename)
    epub.writestr('OEBPS/content.opf', content_info % {
        'manifest': manifest,
        'spine': spine, },
        compress_type=zipfile.ZIP_STORED)


def create_stylesheet(epub):
    css_info = '''
        body {
          font-family: sans-serif;     
        }
        h1,h2,h3,h4 {
          font-family: serif;     
          color: red;
        }
    '''
    epub.writestr('OEBPS/stylesheet.css', css_info,
                  compress_type=zipfile.ZIP_STORED)


def create_archive(path):
    epub_name = '%s.epub' % os.path.basename(path)
    os.chdir(path)
    epub = zipfile.ZipFile(epub_name, 'w')
    create_mimetype(epub)
    create_container(epub)
    create_content(epub, path)
    create_stylesheet(epub)
    for html in os.listdir('.'):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            epub.write(html, 'OEBPS/' + basename,
                       compress_type=zipfile.ZIP_DEFLATED)
    epub.close()


if __name__ == '__main__':
    path = r'E:\hello_world\Learn Spider\pdf'
    create_archive(path)
