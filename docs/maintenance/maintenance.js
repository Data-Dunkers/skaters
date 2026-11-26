const API_URL = 'https://api.datadunkers.ca';
const maintenancePasswordHash = '009f52be6bfdc5450d1562ce55d489fb96580097ae1437a5ac781d37929bd9ec';
const eventKey = localStorage.getItem('event_key')?.trim();
const statusMessage = document.getElementById('maintenance-status');
const nicknameSelect = document.getElementById('lookup-nickname');
const findButton = document.getElementById('find-player');
const lookupStatus = document.getElementById('lookup-status');
const playerResults = document.getElementById('player-results');
const maintenanceContent = document.getElementById('maintenance-content');
const passwordInput = document.getElementById('maintenance-password');
const unlockButton = document.getElementById('unlock-button');
const unlockStatus = document.getElementById('unlock-status');

const submissionGroups = [
    ['photos', 'Photos', {
        real_name: 'Name', group: 'Group', jersey_number: 'Jersey number'
    }],
    ['traits', 'Traits', {
        height_cm: 'Height (cm)', wingspan_cm: 'Wingspan (cm)', skate_size: 'Skate size',
        handedness: 'Handedness', birth_month: 'Birth month', reaction_time_ms: 'Reaction time (ms)',
        resting_heart_rate: 'Resting heart rate (bpm)', group: 'Group'
    }],
    ['shots', 'Shooting', {
        distance: 'Distance (ft)', shots_made: 'Goals made', shots_attempted: 'Shots attempted',
        group: 'Group'
    }],
    ['rocket_league', 'Rocket League', {
        score: 'Score', goals: 'Goals', assists: 'Assists', saves: 'Saves', shots: 'Shots', group: 'Group'
    }]
];

const escapedEvent = eventKey?.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
const eventFilter = "(event_key = '" + escapedEvent + "')";

if (globalThis.crypto?.subtle) {
    unlockButton.disabled = false;
} else {
    unlockStatus.textContent = 'Open this page over HTTPS or on localhost to unlock it.';
}

document.getElementById('unlock-form').addEventListener('submit', async event => {
    event.preventDefault();
    if (unlockButton.disabled || !maintenanceContent.hidden) return;
    unlockButton.disabled = true;
    unlockStatus.textContent = '';
    const password = new TextEncoder().encode(passwordInput.value);
    passwordInput.value = '';
    try {
        const digest = await crypto.subtle.digest('SHA-256', password);
        const hash = Array.from(new Uint8Array(digest), value => value.toString(16).padStart(2, '0')).join('');
        if (hash !== maintenancePasswordHash) {
            unlockStatus.textContent = 'Incorrect password. Try again.';
            return;
        }

        document.getElementById('selected-event').textContent = eventKey || 'None';
        document.getElementById('event-context').hidden = false;
        document.getElementById('maintenance-lock').hidden = true;
        maintenanceContent.hidden = false;
        maintenanceContent.querySelector('.menu button').focus();
        if (eventKey) loadNicknames();
    } catch {
        unlockStatus.textContent = 'Could not check the password. Try again.';
    } finally {
        unlockButton.disabled = false;
        if (maintenanceContent.hidden) passwordInput.focus();
    }
});

const menuButtons = document.querySelectorAll('.menu button');
for (const button of menuButtons) {
    button.addEventListener('click', () => {
        for (const option of menuButtons) {
            const selected = option === button;
            option.setAttribute('aria-pressed', String(selected));
            document.getElementById(option.getAttribute('aria-controls')).hidden = !selected;
        }
    });
}

async function fetchRecords(collection, filter, fields) {
    const records = [];
    for (let page = 1; ; page++) {
        const params = new URLSearchParams({
            filter, fields: fields.join(','), sort: '-created,-id', perPage: '100', page: String(page)
        });
        const response = await fetch(API_URL + '/api/collections/data_skaters_' + collection +
            '/records?' + params, { cache: 'no-store' });
        if (!response.ok) throw new Error('PocketBase request failed.');
        const data = await response.json();
        records.push(...data.items);
        if (page >= data.totalPages) return records;
    }
}

async function loadNicknames() {
    statusMessage.textContent = 'Loading nicknames for this event…';
    const groups = await Promise.allSettled(submissionGroups.map(([key]) =>
        fetchRecords(key, eventFilter, ['nickname'])
    ));
    const nicknames = new Set();
    let failedGroups = 0;
    for (const group of groups) {
        if (group.status === 'rejected') {
            failedGroups++;
            continue;
        }
        for (const { nickname } of group.value) {
            if (typeof nickname === 'string' && nicknamePattern.test(nickname)) {
                nicknames.add(nickname.toUpperCase());
            }
        }
    }

    for (const nickname of [...nicknames].sort()) {
        const option = document.createElement('option');
        option.value = nickname;
        option.textContent = nickname;
        nicknameSelect.append(option);
    }
    nicknameSelect.disabled = nicknames.size === 0;

    if (failedGroups === groups.length || (failedGroups > 0 && nicknames.size === 0)) {
        statusMessage.textContent = 'Could not load the event’s nicknames. Reload the page to try again.';
    } else if (failedGroups > 0) {
        statusMessage.textContent = 'Some nicknames may be missing because a station could not be loaded.';
    } else if (nicknames.size === 0) {
        statusMessage.textContent = 'No valid nicknames were found for this event.';
    } else {
        statusMessage.textContent = '';
    }
}

nicknameSelect.addEventListener('change', () => {
    findButton.disabled = !nicknameSelect.value;
    playerResults.replaceChildren();
    lookupStatus.textContent = '';
});

document.getElementById('lookup-form').addEventListener('submit', async event => {
    event.preventDefault();
    if (maintenanceContent.hidden || !eventKey || findButton.disabled) return;
    const nickname = nicknameSelect.value;
    if (!nicknamePattern.test(nickname)) return;
    nicknameSelect.disabled = true;
    findButton.disabled = true;
    playerResults.replaceChildren();
    lookupStatus.textContent = 'Looking up ' + nickname + '…';
    try {
        // Match legacy mixed-case nicknames without matching part of a nickname.
        const [first, second] = nickname;
        const digits = nickname.slice(2, 4);
        const suffix = nickname.slice(4);
        const suffixCases = suffix ? ['-T', '-t'] : [''];
        const initialCases = [first + second, first.toLowerCase() + second,
            first + second.toLowerCase(), (first + second).toLowerCase()];
        const mixedCases = initialCases.flatMap(initials => suffixCases.map(ending => initials + digits + ending));
        const nicknameFilter = mixedCases.map(value => "nickname = '" + value + "'").join(' || ');
        const filter = eventFilter + ' && (' + nicknameFilter + ')';
        const groups = await Promise.allSettled(submissionGroups.map(([key, , labels]) => {
            const fields = ['id', 'created', ...Object.keys(labels)];
            if (key === 'photos') fields.push('photo');
            if (key === 'shots') fields.push('shots_taken', 'attempts');
            return fetchRecords(key, filter, fields);
        }));
        renderPlayer(nickname, groups);
    } catch {
        lookupStatus.textContent = 'Could not display player records. Try again.';
        playerResults.replaceChildren();
    } finally {
        nicknameSelect.disabled = false;
        findButton.disabled = false;
    }
});

function renderPlayer(nickname, groups) {
    const loaded = groups.filter(group => group.status === 'fulfilled');
    const count = loaded.reduce((total, group) => total + group.value.length, 0);
    if (loaded.length === 0) {
        lookupStatus.textContent = 'Could not load player records. Try again.';
        return;
    }
    if (count === 0 && loaded.length === groups.length) {
        lookupStatus.textContent = 'No submissions for ' + nickname + ' in this event.';
        return;
    }
    lookupStatus.textContent = nickname + ' · ' + count + (count === 1 ? ' submission' : ' submissions');
    if (loaded.length < groups.length) lookupStatus.textContent += ' · Some results could not be loaded';

    for (const [index, [key, title, fields]] of submissionGroups.entries()) {
        const group = groups[index];
        const section = document.createElement('section');
        section.className = 'result-section';
        const heading = document.createElement('h3');
        heading.textContent = group.status === 'fulfilled' ? title + ' (' + group.value.length + ')' : title;
        section.append(heading);
        playerResults.append(section);

        if (group.status === 'rejected') {
            const failure = document.createElement('p');
            failure.textContent = 'Could not load these submissions.';
            section.append(failure);
            continue;
        }
        for (const record of group.value) {
            const submission = document.createElement('article');
            submission.className = 'submission';
            const submitted = document.createElement('h4');
            const date = new Date(record.created.replace(' ', 'T'));
            submitted.textContent = Number.isNaN(date.getTime()) ? record.id : date.toLocaleString();
            submission.append(submitted);

            if (key === 'shots') {
                record.shots_attempted ??= record.shots_taken ?? record.attempts;
            }

            const details = document.createElement('dl');
            for (const [field, label] of Object.entries(fields)) {
                if (record[field] === undefined || record[field] === null || record[field] === '') continue;
                const pair = document.createElement('div');
                const term = document.createElement('dt');
                const value = document.createElement('dd');
                term.textContent = label;
                value.textContent = record[field];
                pair.append(term, value);
                details.append(pair);
            }
            if (details.childElementCount) submission.append(details);

            if (key === 'photos' && record.photo) {
                const photo = document.createElement('a');
                photo.href = API_URL + '/api/files/data_skaters_photos/' +
                    encodeURIComponent(record.id) + '/' + encodeURIComponent(record.photo);
                photo.textContent = 'Open photo';
                photo.target = '_blank';
                photo.rel = 'noreferrer';
                submission.append(photo);
            }
            section.append(submission);
        }
    }
}
