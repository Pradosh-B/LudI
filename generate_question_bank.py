import json
from pathlib import Path

source = Path('LUDUS_INTELLECTUS_question_bank.json')
raw = json.loads(source.read_text(encoding='utf-8'))

diff_map = {
    'easy': 'Easy',
    'medium': 'Medium',
    'hard': 'Hard',
}

rows = []
for idx, q in enumerate(raw.get('questions', []), start=1):
    options = q.get('options') or ['', '', '', '']
    if len(options) < 4:
        options = options + [''] * (4 - len(options))

    ans = str(q.get('answer') or 'A').strip().upper()
    if ans not in 'ABCD':
        ans = 'A'

    rows.append({
        'q': q.get('question') or '',
        'a': options[0],
        'b': options[1],
        'c': options[2],
        'd': options[3],
        'ans': ans,
        'cat': q.get('topic') or 'General Knowledge',
        'diff': diff_map.get((q.get('difficulty') or 'easy').lower(), 'Easy'),
        'id': idx,
    })

Path('question_bank_generated.js').write_text(
    'window.LUDUSQuestionBank = ' + json.dumps(rows, ensure_ascii=False) + ';\n',
    encoding='utf-8'
)

print(f'generated={len(rows)}')
