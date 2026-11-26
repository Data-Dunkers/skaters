const nicknamePattern = /^[A-Z]{2}[0-9]{2}(-T)?$/i;
const nicknameFormatMessage = 'Use two letters and two digits, with an optional -T for teachers.';

function sanitizeNickname(value) {
    const [base, ...suffix] = value.toUpperCase().split('-');
    const cleaned = base.replace(/[^A-Z0-9]/g, '');
    let result = '';
    for (const ch of cleaned) {
        const isLetter = /[A-Z]/.test(ch);
        if (result.length < 2 ? isLetter : (result.length < 4 && !isLetter)) {
            result += ch;
        }
    }
    return [result, ...suffix].join('-');
}
