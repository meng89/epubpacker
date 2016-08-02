# coding=utf-8

# Image Types
GIF = 'image/gif'  # ['.gif'], 'Images'],
JPEG = 'image/jpeg'  # ['.jpg', 'jpeg'], 'Images'],
PNG = 'image/png'  # ['.png'], 'Images'],
SVG = 'image/svg+xml'  # ['.svg'], 'Images'],

# Application Types
XHTML = 'application/xhtml+xml'  # ['.html', '.xhtml'], 'Text'],
FONT_SFNT = 'application/font-sfnt'  # ['.otf', '.ttf', '.ttc'], 'Fonts'],  # old 'application/vnd.ms-opentype'
FONT_WOFF = 'application/font-woff'  # ['.woff'], 'Fonts'],
SMIL = 'application/smil+xml'  # [], 'Text'],  # EPUB Media Overlay documents
PLS = 'application/pls+xml'  # [], ''],  # Text-to-Speech (TTS) Pronunciation lexicons

# ncx
NCX = 'application/x-dtbncx+xml'  # [], ''],

# Audio Types
MP3 = 'audio/mpeg'  # ['.mp3'], ''],
AAC = 'audio/mp4'  # ['.mp4'], ''],

# Text Types
HTML = 'text/html'  # [], 'Text'],
CSS = 'text/css'  # ['.css'], 'Styles'],
JS = 'text/javascript'  # ['.js'], 'Scripts'],

# Font Types
FONT_WOFF2 = 'font/woff2'  # ['.woff2'], 'Fonts'],


map_from_extension = {
    '.gif': GIF,
    '.jpg''.jpeg': JPEG, '.jpeg': JPEG,
    '.png': PNG,
    '.svg': SVG,

    '.xhtml': XHTML,
    '.otf': FONT_SFNT, '.ttf': FONT_SFNT, '.ttc': FONT_SFNT,
    '.woff': FONT_WOFF,
    '.smil': SMIL, '.smi': SMIL,
    '.pls': PLS,

    '.ncx': NCX,

    '.mp3': MP3,
    '.aac': AAC,

    '.html': HTML,
    '.css': CSS,
    '.js': JS,

    '.woff2': FONT_WOFF2
}
