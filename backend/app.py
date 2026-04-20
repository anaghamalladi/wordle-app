from flask import Flask, jsonify, request, after_this_request
from flask_cors import CORS
import random
import urllib.request

app = Flask(__name__)
CORS(app)

WORD_LIST = [
    "crane", "slate", "audio", "raise", "stare",
    "bland", "crimp", "globe", "hasty", "knelt",
    "lucid", "mogul", "notch", "jazzy", "flowy",
    "abbey", "favor", "merit", "optic", "plumb",
    "queen", "risky", "shelf", "tiger", "umbra",
    "vapor", "waltz", "xenon", "yacht", "zonal",
    "blaze", "civic", "drawl", "epoch", "flair",
    "gloom", "hinge", "infer", "joust", "knack",
    "latch", "maxim", "nerve", "onset", "pixel",
    "qualm", "resin", "snare", "trove", "ulcer",
    "visor", "whirl", "expel", "yearn", "zesty",
    "abide", "brisk", "chord", "dodge", "ember",
    "fjord", "gruel", "humid", "ionic", "jerky",
    "karma", "libel", "mirth", "noble", "oxide",
    "perch", "quirk", "rover", "swamp", "tabby",
    "unify", "venom", "wrath", "extol"
]

secret_word = random.choice(WORD_LIST)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/word", methods=["GET"])
def get_word():
    return jsonify({"word": secret_word})

@app.route("/guess", methods=["POST", "OPTIONS"])
def check_guess():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.get_json()
    guess = data.get("guess", "").lower()

    if len(guess) != 5:
        return jsonify({"error": "Guess must be 5 letters"}), 400

    result = []
    for i in range(5):
        if guess[i] == secret_word[i]:
            result.append({"letter": guess[i], "status": "correct"})
        elif guess[i] in secret_word:
            result.append({"letter": guess[i], "status": "present"})
        else:
            result.append({"letter": guess[i], "status": "absent"})

    return jsonify({"result": result})

VALID_WORDS = set([
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
    "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
    "alike", "align", "alley", "allow", "alone", "along", "alter", "angel",
    "anger", "angle", "angry", "anime", "ankle", "annex", "apart", "apple",
    "apply", "arena", "argue", "arise", "armor", "army", "aroma", "arose",
    "array", "aside", "asset", "atlas", "attic", "audio", "audit", "avoid",
    "awake", "award", "aware", "awful", "badly", "baker", "bases", "basic",
    "basis", "beach", "began", "begin", "being", "below", "bench", "billy",
    "birth", "black", "blade", "blame", "bland", "blank", "blast", "blaze",
    "bleed", "blend", "bless", "blind", "block", "blood", "bloom", "blown",
    "blues", "blunt", "board", "bonus", "boost", "booth", "bound", "brain",
    "brand", "brave", "bread", "break", "breed", "brick", "bride", "brief",
    "bring", "brisk", "broad", "broke", "brook", "brown", "brush", "buddy",
    "build", "built", "burst", "buyer", "cabin", "camel", "candy", "carry",
    "catch", "cause", "cease", "chair", "chalk", "chaos", "charm", "chart",
    "chase", "cheap", "check", "cheek", "chess", "chest", "chief", "child",
    "china", "choir", "chord", "civil", "claim", "clamp", "clash", "class",
    "clean", "clear", "clerk", "click", "cliff", "climb", "cling", "clock",
    "clone", "close", "cloth", "cloud", "coach", "coast", "cobra", "color",
    "comic", "coral", "count", "court", "cover", "craft", "crane", "crash",
    "crazy", "cream", "creek", "crime", "crimp", "cross", "crowd", "crown",
    "cruel", "crush", "curve", "cycle", "daily", "dance", "dealt", "death",
    "debut", "delta", "depot", "depth", "derby", "devil", "disco", "dodge",
    "doing", "doubt", "dough", "draft", "drain", "drama", "drank", "drawl",
    "dream", "dress", "drift", "drink", "drive", "drone", "drove", "drown",
    "drunk", "dryer", "dying", "eager", "early", "earth", "eight", "elite",
    "ember", "empty", "enemy", "enjoy", "enter", "entry", "epoch", "equal",
    "error", "essay", "event", "every", "exact", "exist", "extra", "fable",
    "faced", "faith", "false", "fancy", "fatal", "fault", "feast", "fence",
    "fever", "fiber", "field", "fifth", "fifty", "fight", "final", "first",
    "fixed", "flair", "flame", "flash", "fleet", "flesh", "flock", "flood",
    "floor", "floss", "flour", "fluid", "flute", "focus", "force", "forge",
    "forth", "forty", "forum", "found", "frame", "frank", "fraud", "fresh",
    "front", "froze", "fruit", "fully", "funny", "ghost", "given", "glass",
    "gloom", "glory", "glove", "going", "grace", "grade", "grain", "grand",
    "grant", "graph", "grasp", "grass", "grave", "great", "green", "greet",
    "grief", "grill", "grind", "groan", "groom", "gross", "group", "grove",
    "grown", "gruel", "guard", "guess", "guest", "guide", "guild", "guilt",
    "guise", "gusto", "habit", "happy", "harsh", "hasty", "haven", "heart",
    "heavy", "hence", "hinge", "hippo", "homer", "honor", "horse", "hotel",
    "house", "human", "humid", "humor", "hurry", "hyper", "ideal", "image",
    "imply", "inbox", "index", "indie", "infer", "inner", "input", "intel",
    "inter", "intro", "ionic", "issue", "ivory", "jazzy", "joust", "judge",
    "juice", "juicy", "karma", "kayak", "knack", "kneel", "knelt", "knife",
    "knock", "knoll", "known", "label", "large", "laser", "later", "latch",
    "laugh", "layer", "leach", "leads", "learn", "lease", "leave", "legal",
    "lemon", "level", "light", "limit", "linen", "liver", "local", "lodge",
    "logic", "loose", "lover", "lower", "loyal", "lucid", "lucky", "lunar",
    "lunch", "lying", "magic", "major", "maker", "manor", "maple", "march",
    "marry", "match", "maxim", "mayor", "media", "mercy", "merit", "metal",
    "might", "minor", "minus", "mirth", "model", "money", "month", "moral",
    "motor", "mount", "mouse", "mouth", "moved", "movie", "muddy", "music",
    "naive", "naked", "nasty", "naval", "nerve", "never", "night", "ninja",
    "noble", "noise", "north", "notch", "noted", "novel", "nurse", "nymph",
    "occur", "ocean", "offer", "often", "onset", "opera", "optic", "orbit",
    "order", "other", "outer", "oxide", "ozone", "paint", "panel", "panic",
    "paper", "party", "pasta", "patch", "pause", "peace", "pearl", "penny",
    "perch", "phase", "phone", "photo", "piano", "pilot", "pitch", "pixel",
    "pizza", "place", "plain", "plane", "plant", "plate", "plaza", "plead",
    "pluck", "plumb", "plume", "plunk", "point", "polar", "posed", "power",
    "press", "price", "pride", "prime", "print", "prior", "prize", "probe",
    "prone", "proof", "prose", "proud", "prove", "psalm", "pubic", "pulse",
    "punch", "pupil", "purse", "qualm", "queen", "query", "quest", "queue",
    "quick", "quiet", "quirk", "quota", "quote", "radar", "radio", "raise",
    "rally", "ranch", "range", "rapid", "ratio", "reach", "ready", "realm",
    "rebel", "recap", "reign", "relax", "repay", "resin", "rider", "ridge",
    "rifle", "right", "rigid", "risky", "rival", "river", "robot", "rocky",
    "rouge", "rough", "round", "rover", "rowdy", "royal", "ruler", "rural",
    "sadly", "saint", "salad", "sauce", "scale", "scare", "scene", "scope",
    "score", "sense", "serve", "setup", "seven", "shade", "shake", "shame",
    "shape", "share", "shark", "sharp", "shelf", "shell", "shift", "shine",
    "shirt", "shock", "shoot", "shore", "short", "shout", "sight", "since",
    "sixth", "sixty", "skill", "skull", "slate", "slave", "sleek", "sleep",
    "slice", "slide", "slope", "smart", "smell", "smile", "smoke", "snake",
    "snare", "solar", "solid", "solve", "sonic", "sorry", "south", "space",
    "spare", "spark", "speak", "speed", "spend", "spice", "spike", "spine",
    "spite", "split", "spoke", "spoon", "spore", "sport", "spray", "squad",
    "stack", "staff", "stage", "stain", "stair", "stake", "stale", "stall",
    "stamp", "stand", "stare", "start", "state", "stays", "steam", "steel",
    "steep", "steer", "stern", "still", "stock", "stomp", "stone", "stood",
    "storm", "story", "stove", "strap", "straw", "stray", "strip", "stuck",
    "study", "stuff", "style", "sugar", "suite", "sunny", "super", "surge",
    "swamp", "swear", "sweep", "sweet", "swift", "swipe", "swirl", "sword",
    "swore", "sworn", "swung", "tabby", "table", "taboo", "talon", "tapir",
    "taste", "teach", "tease", "teeth", "thank", "theme", "there", "these",
    "thick", "thing", "think", "third", "thorn", "those", "three", "threw",
    "throw", "tiger", "tight", "timer", "title", "today", "token", "topic",
    "total", "touch", "tough", "towel", "tower", "toxic", "trace", "track",
    "trade", "trail", "train", "trait", "trash", "treat", "trend", "trial",
    "tribe", "trick", "tried", "troop", "trove", "truce", "truly", "trump",
    "trunk", "trust", "truth", "tumor", "tuner", "twice", "twist", "tying",
    "ulcer", "ultra", "umbra", "unify", "union", "unite", "unity", "until",
    "upper", "upset", "urban", "usage", "usual", "utter", "valid", "value",
    "valve", "vapor", "vault", "venom", "verse", "video", "vigor", "viral",
    "virus", "visor", "visit", "vista", "vital", "vivid", "vocal", "voice",
    "voter", "waltz", "waste", "watch", "water", "weary", "weave", "wedge",
    "weird", "whale", "wheat", "wheel", "where", "which", "while", "white",
    "whole", "whose", "wider", "witch", "woman", "women", "woods", "world",
    "worry", "worse", "worst", "worth", "would", "wound", "wrath", "wrist",
    "write", "wrote", "xenon", "yacht", "yearn", "yield", "young", "yours",
    "youth", "zesty", "zonal"
])

@app.route("/validate", methods=["POST"])
def validate_word():
    data = request.get_json()
    word = data.get("word", "").lower()
    if len(word) != 5:
        return jsonify({"valid": False})
    # Accept any 5-letter alphabetic word
    return jsonify({"valid": word.isalpha()})

if __name__ == "__main__":
    app.run(debug=True, port=5001)