/**
 * My Buddy — Morphology Engine
 *
 * Turns the grammar keys (+S +ING +ED +ER +EST, TO+) into REAL inflected
 * words instead of speaking "walk, ing". Handles English spelling rules and
 * the common irregulars an AAC user actually needs.
 *
 * inflect('run', 'ING')  -> 'running'
 * inflect('make', 'ED')  -> 'made'
 * inflect('go',   'ED')  -> 'went'
 * inflect('big',  'EST') -> 'biggest'
 * inflect('child','S')   -> 'children'
 */

// ── Irregulars (memorized forms; no rule produces these) ──
const IRREGULAR = {
  S: {
    child: 'children', person: 'people', man: 'men', woman: 'women',
    foot: 'feet', tooth: 'teeth', mouse: 'mice', goose: 'geese',
    is: 'are', has: 'have', was: 'were', this: 'these', that: 'those'
  },
  ED: {
    go: 'went', do: 'did', have: 'had', has: 'had', is: 'was', are: 'were',
    am: 'was', make: 'made', get: 'got', give: 'gave', take: 'took',
    come: 'came', see: 'saw', eat: 'ate', drink: 'drank', run: 'ran',
    sit: 'sat', stand: 'stood', find: 'found', think: 'thought',
    feel: 'felt', say: 'said', tell: 'told', know: 'knew', put: 'put',
    read: 'read', let: 'let', hit: 'hit', cut: 'cut', hurt: 'hurt',
    buy: 'bought', bring: 'brought', catch: 'caught', teach: 'taught',
    sleep: 'slept', leave: 'left', lose: 'lost', win: 'won', hold: 'held',
    ride: 'rode', write: 'wrote', drive: 'drove', fly: 'flew', wear: 'wore',
    fall: 'fell', break: 'broke', speak: 'spoke', choose: 'chose',
    swim: 'swam', throw: 'threw', grow: 'grew', draw: 'drew', hear: 'heard',
    build: 'built', send: 'sent', spend: 'spent', keep: 'kept', mean: 'meant'
  },
  ING: {
    // irregular stems for -ing (most are regular; these drop/keep oddly)
    be: 'being', see: 'seeing', flee: 'fleeing'
  },
  ER: { good: 'better', bad: 'worse', far: 'farther', little: 'less', much: 'more' },
  EST: { good: 'best', bad: 'worst', far: 'farthest', little: 'least', much: 'most' }
};

const VOWELS = 'aeiou';
const isVowel = c => VOWELS.indexOf(c) !== -1;

function endsWithCVC(w) {
  // consonant-vowel-consonant, last consonant not w/x/y (for doubling)
  if (w.length < 3) return false;
  const a = w[w.length - 3], b = w[w.length - 2], c = w[w.length - 1];
  return !isVowel(a) && isVowel(b) && !isVowel(c) && 'wxy'.indexOf(c) === -1;
}

function addS(w) {
  if (/[^aeiou]y$/.test(w)) return w.slice(0, -1) + 'ies';      // carry->carries
  if (/(s|sh|ch|x|z)$/.test(w)) return w + 'es';                 // box->boxes
  if (/(f)$/.test(w)) return w.slice(0, -1) + 'ves';             // leaf->leaves
  if (/fe$/.test(w)) return w.slice(0, -2) + 'ves';              // knife->knives
  return w + 's';
}

function addING(w) {
  if (/ie$/.test(w)) return w.slice(0, -2) + 'ying';            // lie->lying
  if (/[^aeiou]e$/.test(w) && w !== 'be') return w.slice(0, -1) + 'ing'; // make->making
  if (endsWithCVC(w)) return w + w[w.length - 1] + 'ing';       // run->running
  return w + 'ing';
}

function addED(w) {
  if (/e$/.test(w)) return w + 'd';                             // like->liked
  if (/[^aeiou]y$/.test(w)) return w.slice(0, -1) + 'ied';      // carry->carried
  if (endsWithCVC(w)) return w + w[w.length - 1] + 'ed';        // stop->stopped
  return w + 'ed';
}

function addER(w) {
  if (/e$/.test(w)) return w + 'r';                             // nice->nicer
  if (/[^aeiou]y$/.test(w)) return w.slice(0, -1) + 'ier';      // happy->happier
  if (endsWithCVC(w)) return w + w[w.length - 1] + 'er';        // big->bigger
  return w + 'er';
}

function addEST(w) {
  if (/e$/.test(w)) return w + 'st';
  if (/[^aeiou]y$/.test(w)) return w.slice(0, -1) + 'iest';
  if (endsWithCVC(w)) return w + w[w.length - 1] + 'est';
  return w + 'est';
}

const RULES = { S: addS, ING: addING, ED: addED, ER: addER, EST: addEST };

/**
 * Inflect a base word by a grammar key.
 * @param {string} word - the base word (may include leading caps)
 * @param {string} key  - one of S, ING, ED, ER, EST, TO
 * @returns {string} the inflected word (TO returns "to <word>")
 */
export function inflect(word, key) {
  if (!word) return word;
  const K = String(key).toUpperCase().replace(/[^A-Z]/g, '');
  if (K === 'TO') return 'to ' + word;

  // preserve leading capital
  const cap = word[0] === word[0].toUpperCase() && word[0] !== word[0].toLowerCase();
  const lower = word.toLowerCase();

  let out;
  if (IRREGULAR[K] && IRREGULAR[K][lower]) {
    out = IRREGULAR[K][lower];
  } else if (RULES[K]) {
    out = RULES[K](lower);
  } else {
    out = word; // unknown key: no-op
  }
  return cap ? out[0].toUpperCase() + out.slice(1) : out;
}

/** Map a tile's action string ("+ing","+S","to+") to a rule key, else null. */
export function actionToKey(action) {
  if (!action || typeof action !== 'string') return null;
  const a = action.toLowerCase().replace(/[+\s]/g, '');
  const map = { s: 'S', ing: 'ING', ed: 'ED', er: 'ER', est: 'EST', to: 'TO', nt: 'NT' };
  return map[a] || null;
}

/** Apply n't as a contraction on auxiliaries (do->don't, is->isn't...). */
export function applyNot(word) {
  if (!word) return word;
  const w = word.toLowerCase();
  const special = {
    will: "won't", can: "can't", shall: "shan't", may: "may not",
    do: "don't", does: "doesn't", did: "didn't", is: "isn't", are: "aren't",
    was: "wasn't", were: "weren't", have: "haven't", has: "hasn't",
    had: "hadn't", would: "wouldn't", could: "couldn't", should: "shouldn't",
    must: "mustn't", might: "might not", am: "am not"
  };
  return special[w] || word + "n't";
}
