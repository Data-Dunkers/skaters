function paintEventKeyBackground(key) {
    const old = document.getElementById('event-key-bg');
    if (old) old.remove();
    if (!key) return;
    const esc = key.replace(/[&<>"']/g, c => `&#${c.charCodeAt(0)};`);
    const w = 260, h = 90;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">` +
        `<g font-family="Barlow Condensed, sans-serif" font-weight="800" font-size="30" fill="#fff" fill-opacity="0.09" text-anchor="middle">` +
        `<text x="${w / 2}" y="35" transform="rotate(-12 ${w / 2} 35)">${esc}</text>` +
        `<text x="0" y="${h - 5}" transform="rotate(-12 0 ${h - 5})">${esc}</text>` +
        `<text x="${w}" y="${h - 5}" transform="rotate(-12 ${w} ${h - 5})">${esc}</text>` +
        `</g></svg>`;
    const layer = document.createElement('div');
    layer.id = 'event-key-bg';
    layer.setAttribute('aria-hidden', 'true');
    layer.style.cssText = 'position:fixed;inset:0;z-index:0;pointer-events:none;' +
        `background-image:url("data:image/svg+xml,${encodeURIComponent(svg)}");background-size:${w}px ${h}px;`;
    document.body.prepend(layer);
    Array.from(document.body.children).forEach(el => {
        if (el === layer || el.tagName === 'SCRIPT') return;
        if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
        if (!el.style.zIndex) el.style.zIndex = 1;
    });
}

window.addEventListener('DOMContentLoaded', () => {
    paintEventKeyBackground(localStorage.getItem('event_key'));
});
