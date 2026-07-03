#!/usr/bin/env python3
"""Generate the My Buddy 84-location (7x12) core system - LAMP Words-for-Life
style: full vocabulary from day one, fixed motor plans, sequenced second-hit
pages. Edit LAYOUT/PAGES below (e.g. to match a child's real WFL device),
re-run, commit. Symbols are verified to exist; missing ones are reported and
skipped, never shipped wrong."""
import json, os, uuid, sys

ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MULB = json.load(open(f"{ROOTDIR}/src/api/mulberry-symbols.json"))
IDX = {e["id"].lower(): e["src"] for e in MULB}
OWNED = f"{ROOTDIR}/public/symbols/mybuddy"

def my(n): return f"/symbols/mybuddy/{n}.svg"
def mul(*cands):
    for w in cands:
        hits = [s for i, s in IDX.items()
                if i.endswith("." + w) or s.endswith("/" + w + ".svg")
                or s.endswith("/" + w + "_,_to.svg") or s.endswith("/" + w.replace("_","-") + ".svg") or s.endswith("/" + w + "_1.svg")]
        if hits: return sorted(hits, key=len)[0]
    return None
def sym(spec):
    if spec is None: return None
    if isinstance(spec, tuple): return mul(*spec)
    p = my(spec)
    return p if os.path.exists(f"{ROOTDIR}/public{p}") else None

# Fitzgerald key
YEL="rgb(255,241,118)"; GRN="rgb(165,214,167)"; BLU="rgb(144,202,249)"
PNK="rgb(244,143,177)"; PUR="rgb(206,147,216)"; RED="rgb(239,154,154)"
ORG="rgb(255,183,77)";  GRY="rgb(224,224,224)"; WHT="rgb(250,250,250)"

def w(label, spec, color, load=None):
    return {"label": label, "spec": spec, "color": color, "load": load}

# ── THE 84-LOCATION MAIN GRID (7 rows x 12 cols) ──
LAYOUT = [
 [w("I","i",YEL),w("you","you",YEL),w("my","my",YEL),w("it","it",YEL),w("we","we",YEL),w("he","he",YEL),w("she","she",YEL),w("they","they",YEL),w("what","what",PUR),w("who","who",PUR),w("where",("where",),PUR),w("when","when",PUR)],
 [w("want","want",GRN),w("like","like",GRN),w("go","go",GRN),w("get","get",GRN),w("help","help",GRN),w("make","make",GRN),w("eat",("eat","eating","dinner"),GRN),w("drink","drink",GRN),w("play","play",GRN),w("stop","stop",RED),w("more","more",GRN),w("again","again",GRN)],
 [w("do","do",GRN),w("can","can",GRN),w("put","put",GRN),w("give","give",GRN),w("take","take",GRN),w("look","look",GRN),w("say","say",GRN),w("feel","feel",GRN),w("know","know",GRN),w("open","open",GRN),w("turn","turn",GRN),w("come","come",GRN)],
 [w("is","is",GRY),w("not","not",RED),w("this","this",YEL),w("that","that",YEL),w("big","big",BLU),w("little","little",BLU),w("good","good",BLU),w("bad","bad",BLU),w("hot","hot",BLU),w("cold","cold",BLU),w("fast","fast",BLU),w("slow","slow",BLU)],
 [w("on","on",PNK),w("in","in",PNK),w("off","off",PNK),w("out","out",PNK),w("up","up",PNK),w("down","down",PNK),w("here","here",PNK),w("some","some",BLU),w("all","all",BLU),w("now","now",BLU),w("later","later",BLU),w("why","why",PUR)],
 [w("yes","yes",GRN),w("no","no",RED),w("please","please",WHT),w("thank you","thank_you",WHT),w("hi","hi",WHT),w("bye","bye",WHT),w("love","love",WHT),w("same","same",BLU),w("different","different",BLU),w("how","how",PUR),w("all done","all_done",GRN),w("sleep","sleep",GRN)],
 [w("Food",("food",),ORG,"wfl-food"),w("Feelings","happy",ORG,"wfl-feelings"),w("People","people",ORG,"wfl-people"),w("Places","places",ORG,"wfl-places"),w("Things","things",ORG,"wfl-things"),w("Animals","animals",ORG,"wfl-animals"),w("Body","body",ORG,"wfl-body"),w("Clothes","clothes",ORG,"wfl-clothes"),w("School","school",ORG,"wfl-school"),w("Colors","colors",ORG,"wfl-colors"),w("read","read",GRN),w("wash","wash",GRN)],
]

# ── SECOND-HIT PAGES (fixed 12-col grids, back always top-left) ──
PAGES = {
 "wfl-food": [w(l,(l.replace(" ",""),),ORG) for l in
   ["apple","banana","bread","milk","water","cheese","pizza","chicken","pasta","cereal","yogurt","crackers"]]
   + [w("cookie","cookie",ORG), w("ice cream",("icecream","ice_cream"),ORG), w("juice",("orangejuice","juice"),ORG)],
 "wfl-feelings": [w(l,l,GRN) for l in ["happy","sad","angry","tired","scared","sick","hungry","hurt"]],
 "wfl-people": [w("mom",("mum","mother"),YEL),w("dad",("dad",),YEL),w("teacher",("teacher",),YEL),
   w("brother",("brother",),YEL),w("sister",("sister",),YEL),w("baby",("baby",),YEL),
   w("grandma",("grandma","granny","grandmother"),YEL),w("grandpa",("grandpa","grandad","grandfather"),YEL),
   w("doctor",("doctor",),YEL),w("boy","boy",YEL),w("girl","girl",YEL),w("friend",("friends","friend","bestfriends"),YEL)],
 "wfl-places": [w("home",("house","home"),ORG),w("school","school",ORG),w("park","park",ORG),
   w("shop",("shop","supermarket"),ORG),w("outside",("outside","garden"),ORG),w("bathroom",("toilet",),ORG),
   w("bedroom","bedroom",ORG),w("kitchen","kitchen",ORG),w("car",("car",),ORG),
   w("bus",("bus",),ORG),w("beach",("beach",),ORG)],
 "wfl-things": [w("ball",("ball",),BLU),w("book","book_g",BLU),w("toy",("teddy","toybox"),BLU),
   w("tablet",("tablet","computer"),BLU),w("tv","tv",BLU),w("blanket",("blanket",),BLU),
   w("shoes","shoes",BLU),w("cup","cup",BLU),w("bubbles",("bubbles",),BLU),
   w("music",("music",),BLU),w("swing",("swing","swings"),BLU),w("phone",("mobilephone","telephone","phone"),BLU)],
 "wfl-animals": [w(l,(l,),PNK) for l in ["dog","cat","bird","fish","horse","cow","rabbit","duck","frog","lion","elephant"]] + [w("pig","pig",PNK)],
 "wfl-body": [w(l, c if isinstance(c,tuple) else (c,), YEL) for l,c in [("head","head"),("hand",("hand","hands")),("foot","foot"),("arm","arm"),("leg","leg"),("eyes","eyes"),("ear","ear"),("nose",("nose","runnynose")),("mouth","mouth"),("tummy",("tummy","stomach","belly")),("hair",("hair","brown_hair")),("teeth","teeth")]],
 "wfl-clothes": [w(l, c if isinstance(c,tuple) else (c,), BLU) for l,c in [("shirt",("tshirt","t_shirt","shirt")),("pants","trousers"),("socks","socks"),("coat","coat"),("hat",("hat","sunhat")),("dress","dress"),("pajamas","pyjamas"),("jumper","jumper")]] + [w("shoes","shoes",BLU)],
 "wfl-school": [w(l, c if isinstance(c,tuple) else (c,), PUR) for l,c in [("pencil","pencil"),("paper","paper"),("scissors","scissors"),("glue","glue"),("crayons",("crayons","waxcrayons","crayon")),("desk","desk"),("bag",("backpack","schoolbag","bag")),("teacher","teacher"),("computer","computer"),("lunch","lunchbox")]],
 "wfl-colors": [],  # filled below with authored swatches
}

# authored color swatches
COLORS=[("red","#e53935"),("blue","#1e88e5"),("green","#43a047"),("yellow","#fdd835"),
 ("orange","#fb8c00"),("purple","#8e24aa"),("pink","#ec407a"),("brown","#6d4c41"),
 ("black","#212121"),("white","#fafafa")]
for name,hexc in COLORS:
    open(f"{OWNED}/color_{name}.svg","w").write(
     f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
     f'<circle cx="24" cy="24" r="16" fill="{hexc}" stroke="#1a1a1a" stroke-width="3"/></svg>')
    PAGES["wfl-colors"].append(w(name, f"color_{name}", WHT))

def build_board(bid, name, rows_spec, cols=12, with_back=True):
    tiles, skipped = [], []
    if with_back:
        tiles.append({"id": f"{bid}-back", "labelKey": "back", "image": my("back"),
                      "backgroundColor": GRY, "loadBoard": "root"})
    flat = rows_spec if isinstance(rows_spec[0], dict) else [c for r in rows_spec for c in r]
    for cell in flat:
        img = sym(cell["spec"])
        if not img:
            skipped.append(cell["label"]); continue
        t = {"id": f"{bid}-{uuid.uuid4().hex[:8]}", "labelKey": cell["label"],
             "image": img, "backgroundColor": cell["color"]}
        if cell["load"]: t["loadBoard"] = cell["load"]
        tiles.append(t)
    rows = (len(tiles) + cols - 1) // cols if with_back else len(rows_spec)
    order = [[tiles[r*cols+c]["id"] if r*cols+c < len(tiles) else None
              for c in range(cols)] for r in range(rows)]
    return {"id": bid, "name": name, "author": "My Buddy", "hidden": False,
            "isPublic": False, "tiles": tiles, "isFixed": True,
            "grid": {"rows": rows, "columns": cols, "order": order}}, skipped

def main():
    d = json.load(open(f"{ROOTDIR}/src/api/boards.json"))
    boards = d["advanced"]
    report = {}
    root, sk = build_board("root", "My Buddy 84", LAYOUT, with_back=False)
    if sk: report["MAIN"] = sk
    boards[:] = [b for b in boards if b.get("id") != "root" and not b.get("id","").startswith("wfl-")]
    boards.insert(0, root)
    for pid, cells in PAGES.items():
        b, sk = build_board(pid, pid.replace("wfl-","").title(), cells)
        if sk: report[pid] = sk
        boards.append(b)
    json.dump(d, open(f"{ROOTDIR}/src/api/boards.json","w"), indent=1)
    print("84-grid main:", len(root["tiles"]), "tiles;", len(PAGES), "second-hit pages")
    print("skipped (no verified symbol):", report or "none")

if __name__ == "__main__":
    main()
