path = "/home/workspace/autonovel/chapters/ch_23.md"
with open(path) as f:
    s = f.read()
orig = s
orig_wc = len(s.split())

# Fix 1: collapse the threefold "It is" anaphora at the end of the throne room scene
old1 = "It is not a statement. It is not a question. It is my name, spoken as if it is the only word he has left. The sound of a man identifying his one, true point of north after centuries of being lost."
new1 = "It is my name, spoken as the only word he has left. The sound of a man identifying his one true north after centuries of being lost."
assert s.count(old1) == 1
s = s.replace(old1, new1, 1)

# Fix 2: collapse the threefold "It is" anaphora at the spring scene early in the chapter
old2 = "It is not the court's map; that survey is complete, its lines inked and fixed. This is a different project. A private one. A projection of a territory I have no authority to chart."
new2 = "It is not the court's map. That survey is complete, its lines inked and fixed. This is a different project: a projection of a territory I have no authority to chart."
assert s.count(old2) == 1
s = s.replace(old2, new2, 1)

# Fix 3: the double "It is" anaphora in the closing line of the throne room scene
old3 = "It is full of him."
# This one is already clean (single short sentence). Leave it.

# Fix 4: the long "It is" anaphora chain at line 144 (largest sound / largest question)
old4 = "It is the smallest sound I have ever heard him make, and the largest question."
new4 = "The smallest sound I have ever heard him make. The largest question."
assert s.count(old4) == 1
s = s.replace(old4, new4, 1)

# Fix 5: the "It is" / "It is" anaphora in "It is not a channel" / "It is an anchor" — leave it,
# it's direct dialogue and part of his character voice.

# Fix 6: collapse the fourfold anaphoric chain in the binding-decision paragraph
old6 = "It is an anchor. And I am a ruin, Sable. You would anchor yourself to a collapsing shore."
# This is in dialogue. Leave it — it's his voice breaking.

# Fix 7: collapse "It is the silence of a map before the first line is drawn."
old7 = "The silence that follows is absolute. It is the silence of a map before the first line is drawn."
new7 = "The silence that follows is the silence of a map before the first line is drawn."
assert s.count(old7) == 1
s = s.replace(old7, new7, 1)

with open(path, "w") as f:
    f.write(s)

new_wc = len(s.split())
print(f"before: {orig_wc} words, after: {new_wc} words, delta: {new_wc - orig_wc}")
