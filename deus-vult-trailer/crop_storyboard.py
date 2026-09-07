from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

source = Image.open('/home/.z/chat-uploads/dv_storyboard-9e7414f573d1.png').convert('RGB')
out = Path(__file__).parent / 'assets' / 'storyboard'
out.mkdir(parents=True, exist_ok=True)

boxes = [
    (0, 0, 340, 272), (390, 0, 675, 272), (710, 0, 1120, 272),
    (1150, 0, 1260, 272), (1305, 0, 1672, 272),
    (0, 272, 330, 504), (390, 272, 500, 504), (540, 272, 720, 504),
    (755, 272, 990, 504), (1065, 272, 1125, 504), (1175, 272, 1325, 504),
    (1350, 272, 1672, 504),
    (0, 504, 330, 736), (390, 504, 495, 736), (540, 504, 715, 736),
    (760, 504, 1120, 736), (1160, 504, 1672, 736), (0, 736, 1672, 941),
]

for i, box in enumerate(boxes, 1):
    im = source.crop(box)
    w, h = im.size
    patch_h = min(30, h // 8)
    if i in {3, 6, 9, 12, 13, 17}:
        patch = im.crop((min(125, w // 3), 0, min(235, w), patch_h)).resize((min(130, w), patch_h))
        im.paste(patch, (0, 0))
    else:
        sample = im.crop((0, patch_h, max(1, min(w, 80)), min(h, patch_h + 18)))
        fill = sample.resize((w, patch_h)).filter(ImageFilter.GaussianBlur(4))
        im.paste(fill, (0, 0))
    im.save(out / f'scene_{i:02d}.jpg', quality=96, subsampling=0)

print(f'Wrote {len(boxes)} cleaned storyboard crops to {out}')
