/* TABLE OF CONTENTS
 * 1. New-run identity  2. Wait for the image  3. Focus Observe exactly once
 * Placeholders are filled by presentation.focus_transport with JSON encoding.
 */
(() => {
  const targetId = __TARGET_ID_JSON__;
  const sectionId = __SECTION_ID_JSON__;
  const host = window.parent;
  const focused = host.__dispersionFocusedRuns || (host.__dispersionFocusedRuns = new Set());
  if (focused.has(targetId)) return;
  let attempts = 0;
  function focus() {
    if (focused.has(targetId)) return;
    const board = host.document.getElementById(targetId);
    const heading = host.document.getElementById(sectionId);
    const image = board && board.querySelector('img');
    if (heading && image && image.complete && image.naturalWidth && board.getBoundingClientRect().height > 0) {
      focused.add(targetId);
      heading.scrollIntoView({block: 'start', behavior: 'instant'});
      return;
    }
    if (++attempts < 100) window.setTimeout(focus, 100);
  }
  window.requestAnimationFrame(() => window.requestAnimationFrame(focus));
})();
