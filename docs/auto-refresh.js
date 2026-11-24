function setupAutoRefresh({ storageKey, interval, refresh }) {
    const toggle = document.getElementById('autorefresh-toggle');
    const countdown = document.getElementById('autorefresh-countdown');
    let timer = null;
    let animation;

    function updateTimer() {
        clearInterval(timer);
        animation?.cancel();
        const enabled = toggle.checked && !toggle.disabled;
        countdown.hidden = !enabled;
        if (!enabled) return;

        animation = countdown.firstElementChild.animate(
            [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }],
            {
                duration: interval,
                easing: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'steps(4, end)' : 'linear',
                fill: 'both'
            }
        );
        timer = setInterval(() => {
            animation.cancel();
            animation.play();
            refresh();
        }, interval);
    }

    toggle.checked = localStorage.getItem(storageKey) === '1';
    toggle.addEventListener('change', () => {
        localStorage.setItem(storageKey, toggle.checked ? '1' : '0');
        updateTimer();
    });
    updateTimer();
}
