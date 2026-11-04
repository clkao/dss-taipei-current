"""Draw the two banner faces with opposite tails and readable lettering."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PHRASES = {'bubble-rest': '叫你休息', 'bubble-listen': '講不聽'}

def write_bubble_artwork(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, text in PHRASES.items():
        right = name == 'bubble-listen'
        image = Image.new('RGBA', (768, 768), 'white')
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((52, 70, 716, 615), radius=135, fill='white', outline='#20272b', width=12)
        points = lambda values: [(768-x if right else x, y) for x, y in values]
        draw.polygon(points([(205,608), (112,700), (325,608)]), fill='white')
        draw.line(points([(205,614), (112,700), (325,614)]), fill='#20272b', width=12)
        lines = ['叫你', '休息'] if name == 'bubble-rest' else ['講不聽']
        size = 205 if len(lines) == 2 else 185
        font = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', size)
        for k, line in enumerate(lines):
            draw.text((384, 265+215*k if len(lines)==2 else 360), line, font=font, fill='#20272b', anchor='mm')
        image.save(directory/(name+'.png'))
        spans = ''.join(f'<text x="384" y="{305+215*k if len(lines)==2 else 405}" text-anchor="middle" font-family="Heiti TC, sans-serif" font-size="{size}" fill="#20272b">{line}</text>' for k, line in enumerate(lines))
        transform = ' transform="translate(768 0) scale(-1 1)"' if right else ''
        (directory/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="15.2mm" height="15.2mm" viewBox="0 0 768 768"><rect width="768" height="768" fill="white"/><path{transform} d="M190 70 H578 Q716 70 716 208 V477 Q716 615 578 615 H325 L112 700 L205 615 H190 Q52 615 52 477 V208 Q52 70 190 70 Z" fill="white" stroke="#20272b" stroke-width="12"/>{spans}</svg>')

if __name__ == '__main__':
    write_bubble_artwork(Path(__file__).resolve().parent/'accessories/tsai-banner')
