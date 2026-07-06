// Bug 1: some saved board/toolbar tiles store their label as the literal text
// "\u2302" / "\uD83D\uDD0A" / "\u232B" instead of the glyph, so the raw escape
// shows on screen. This decodes any literal \uXXXX or \u{XXXXX} at render time,
// so bad saved data self-heals. Surrogate pairs (\uD83D\uDD0A -> 🔊) reassemble
// automatically because JS strings are UTF-16.
//
// Apply where a tile label becomes display text, e.g. in
// src/components/Board/Symbol/Symbol.js before rendering `label`, and in the
// output bar. This does NOT replace fixing the stored data — see README.

export function decodeEscapes(str) {
  if (typeof str !== 'string' || str.indexOf('\\u') === -1) return str;
  return str
    .replace(/\\u\{([0-9a-fA-F]+)\}/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/\\u([0-9a-fA-F]{4})/g,   (_, h) => String.fromCharCode(parseInt(h, 16)));
}

// Intended glyphs for the toolbar buttons seen in the screenshots:
//   \u2302        -> ⌂   (Home)
//   \uD83D\uDD0A  -> 🔊  (Speak)
//   \u232B        -> ⌫   (Backspace)
