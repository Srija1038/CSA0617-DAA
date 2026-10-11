"""Renders terminal-style screenshots of the saved program outputs and editor-style code figures."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__); R = os.path.join(HERE, "..", "results"); F = os.path.join(HERE, "..", "figures")
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"; MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CWD = "~/DAA-A1-192525223-T.Srija/src"


def terminal(txt_file, cmd, out_name):
    lines = open(txt_file).read().rstrip("\n").split("\n")
    fs = 14; font, fb = ImageFont.truetype(MONO, fs), ImageFont.truetype(MONOB, fs)
    cw, lh, pad, bar = font.getlength("M"), 20, 18, 34
    cmdl = f"{CWD}$ {cmd}"
    w = int(max(max(len(l) for l in lines), len(cmdl)) * cw + 2 * pad); h = bar + 2 * pad + lh * (len(lines) + 3)
    im = Image.new("RGB", (w, h), "#0c0c0c"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, bar], fill="#2b2b2b")
    d.text((14, 8), f"Terminal  -  {CWD}", font=ImageFont.truetype(SANS, 12), fill="#d0d0d0")
    for i, c in enumerate(("#ffbd2e", "#27c93f", "#ff5f56")): d.ellipse([w - 24 - i * 20, 11, w - 12 - i * 20, 23], fill=c)
    y = bar + pad
    d.text((pad, y), cmdl, font=fb, fill="#7ee787"); y += lh
    for l in lines:
        col = "#e8e8e8"
        if l.startswith("Reg No") or l.startswith("TASK"): col = "#ffd866"
        if "FAIL" in l and "0" not in l.split("failed:")[-1][:3] and "ALL PASS" not in l: col = "#ff7b72"
        d.text((pad, y), l, font=font, fill=col); y += lh
    y += lh; d.text((pad, y), f"{CWD}$ _", font=font, fill="#7ee787")
    im.save(os.path.join(F, out_name)); print(out_name, im.size)


def code_fig(py_file, out_name, label, first=None, last=None):
    allv = open(py_file).read().rstrip("\n").split("\n")
    a = next((i for i, l in enumerate(allv) if first and first in l), 0)
    z = next((i for i, l in enumerate(allv) if last and last in l), len(allv))
    lines = allv[a:z]
    while lines and not lines[-1].strip(): lines.pop()
    start_no = a + 1
    fs = 14; font = ImageFont.truetype(MONO, fs); cw, lh, pad, bar, gut = font.getlength("M"), 21, 14, 62, 52
    w = int(max(len(l) for l in lines) * cw + gut + 2 * pad + 190); h = bar + pad + lh * len(lines) + pad
    im = Image.new("RGB", (w, h), "#1e1e1e"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 34], fill="#252526"); d.rectangle([0, 34, 230, 62], fill="#1e1e1e")
    d.text((14, 42), os.path.basename(py_file), font=ImageFont.truetype(SANS, 12), fill="#ffffff")
    d.text((14, 9), f"File   Edit   Selection   View   -   {os.path.basename(py_file)}  -  Editor", font=ImageFont.truetype(SANS, 11), fill="#aaaaaa")
    y = bar
    for i, l in enumerate(lines, start_no):
        hi = "basic operation" in l
        if hi: d.rectangle([gut - 6, y - 1, w - 8, y + lh - 2], fill="#5a4a00"); d.rectangle([gut - 6, y - 1, gut - 3, y + lh - 2], fill="#ffcc00")
        d.text((12, y), f"{i:>3}", font=font, fill="#858585")
        code, _, com = l.partition("#")
        col = "#d4d4d4"
        for kw in ("def ", "return", "if ", "for ", "while ", "in ", "import ", "from ", "class "):
            pass
        d.text((gut, y), code, font=font, fill=("#ffffff" if hi else col))
        if com: d.text((gut + font.getlength(code), y), "#" + com, font=font, fill=("#ffe066" if hi else "#6a9955"))
        y += lh
    d.text((w - 180, h - 22), label, font=ImageFont.truetype(SANS, 10), fill="#cccccc")
    im.save(os.path.join(F, out_name)); print(out_name, im.size)


if __name__ == "__main__":
    terminal(f"{R}/out_test.txt", "python3 test_correctness.py", "s_tests.png")
    for n in (1000, 10000, 100000, 1000000):
        terminal(f"{R}/out_bench_{n}.txt", f"python3 benchmark.py --n {n}", f"s_bench_{n}.png")
    terminal(f"{R}/out_task12.txt", "python3 task12.py", "s_task12.png")
    terminal(f"{R}/out_recurrence.txt", "python3 recurrence_check.py", "s_recurrence.png")
    code_fig(f"{HERE}/algo1_linear.py", "s_code_linear.png", "Python  |  UTF-8")
    code_fig(f"{HERE}/algo2_binary.py", "s_code_binary.png", "Python  |  UTF-8", first="def binary_search(", last="def binary_search_iter")
    code_fig(f"{HERE}/algo3_hash_probing.py", "s_code_hash.png", "Python  |  UTF-8", first="def search(")
