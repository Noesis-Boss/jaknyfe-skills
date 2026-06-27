path = "/home/workspace/autonovel/chapters/ch_25.md"
with open(path) as f:
    s = f.read()
orig = s
orig_wc = len(s.split())

# Fix 1: collapse the meta-fractal "It is beautiful, the way a perfectly scaled and accurate map is beautiful"
# (the same adjective applied twice in one sentence)
old1 = "The map takes form. It is beautiful, the way a perfectly scaled and accurate map is beautiful. The true lines form a clean, elegant grid. The phantom lines are chaos, and now I can see exactly where their roots must be severed."
new1 = "The map takes form. The true lines run in a clean, elegant grid; the ph