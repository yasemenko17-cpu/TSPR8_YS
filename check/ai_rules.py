"""Правила перевірки форми й узгодженості матеріалів частини Б (папка my_ai).

Правила перевіряють форму та зв'язки між файлами, а не зміст: чи історія й тест-кейс доречні для продукту,
вирішує викладач. Кожне правило повертає перелік зауважень; порожній перелік означає, що правило виконано.
"""
import datetime
import json
import re
from pathlib import Path

LOG_FIELDS = ("id", "date", "stage", "tool", "request", "data_class", "outcome", "minutes_ai",
              "minutes_manual_est", "defects_caught", "defects_escaped", "note", "artifact")
STAGES = ("історії", "критерії приймання", "тести", "оцінки", "код", "рев'ю", "дослідження відгуків")
CLASSES = ("вигадані", "публічні", "власні", "персональні", "секретні")
OUTCOMES = ("прийнято", "правка", "відхилено")
SOURCES = ("диплом", "власний проєкт", "навчальний кейс")
PLANS = ("безкоштовний", "студентський пакет")
FILES = ("project.json", "ai_log.jsonl", "stories.json", "test_cases.json", "summary.json", "conclusion.md")
HEADINGS = ("Що зроблено", "Що перевірено і виправлено", "Вплив на якість", "Вплив на час")

STORY = re.compile(r"^Як (?P<role>[^,]+), я хочу (?P<goal>.+?), щоб (?P<why>.+)\.$")
GWT = re.compile(r"^Дано .+, коли .+, тоді .+\.$")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"\+?\d[\d\s()-]{8,}\d")
SECRETS = [("ключ API", re.compile(r"\bsk-[A-Za-z0-9]{16,}")),
           ("токен доступу", re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}")),
           ("токен GitHub", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
           ("пароль", re.compile(r"(?i)\b(?:пароль|password|passwd)\s*[:=]\s*\S+"))]


def words(text):
    return len(str(text).split())


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def ids_of(cell):
    return [p for p in re.split(r"[,\s]+", str(cell).strip()) if p]


class Material:
    """Завантажує файли папки; відсутній або пошкоджений файл дає None й зауваження."""

    def __init__(self, folder, today=None):
        self.folder = Path(folder)
        self.today = today or datetime.date.today().isoformat()
        self.errors = []
        self.project = self._json("project.json")
        self.stories = self._json("stories.json")
        self.tests = self._json("test_cases.json")
        self.summary = self._json("summary.json")
        self.log = self._jsonl("ai_log.jsonl")
        path = self.folder / "conclusion.md"
        self.conclusion = path.read_text(encoding="utf-8") if path.exists() else None

    def _json(self, name):
        path = self.folder / name
        if not path.exists():
            self.errors.append(f"немає файлу {name}")
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as e:
            self.errors.append(f"{name}: не є коректним JSON ({e})")
            return None
        if not data:
            self.errors.append(f"{name}: файл порожній")
            return None
        return data

    def _jsonl(self, name):
        path = self.folder / name
        if not path.exists():
            self.errors.append(f"немає файлу {name}")
            return None
        rows = []
        for k, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                self.errors.append(f"{name}: рядок {k} не є коректним JSON")
        if not rows:
            self.errors.append(f"{name}: журнал порожній")
            return None
        return rows


def rule_files(m):
    out = list(m.errors)
    if m.conclusion is None:
        out.append("немає файлу conclusion.md")
    elif not m.conclusion.strip():
        out.append("conclusion.md: файл порожній")
    return out


def rule_project(m):
    p = m.project
    if not isinstance(p, dict):
        return ["project.json: очікується об'єкт"]
    out = []
    if words(p.get("name", "")) < 2:
        out.append("name: назва продукту щонайменше з двох слів")
    if words(p.get("goal", "")) < 4:
        out.append("goal: мета продукту щонайменше з чотирьох слів")
    if p.get("source") not in SOURCES:
        out.append("source: має бути «диплом», «власний проєкт» або «навчальний кейс»")
    if p.get("source") == "навчальний кейс" and p.get("case") not in (1, 2, 3):
        out.append("case: для навчального кейса вкажіть номер контексту 1, 2 або 3")
    if not str(p.get("tool_name", "")).strip():
        out.append("tool_name: не вказано назву асистента")
    if p.get("tool_plan") not in PLANS:
        out.append("tool_plan: має бути «безкоштовний» або «студентський пакет»")
    roles = p.get("roles")
    if not isinstance(roles, list) or len({str(r).strip().lower() for r in roles if str(r).strip()}) < 2:
        out.append("roles: щонайменше дві різні ролі користувачів")
    vocab = p.get("vocabulary")
    if not isinstance(vocab, list) or len([v for v in vocab if str(v).strip()]) < 3:
        out.append("vocabulary: щонайменше три терміни словника продукту")
    priv = p.get("privacy")
    if not isinstance(priv, dict) or priv.get("personal_data_sent") is not False or priv.get("secrets_sent") is not False \
            or priv.get("settings_checked") is not True:
        out.append("privacy: personal_data_sent і secrets_sent мають бути false, settings_checked true")
    return out


def _texts(m):
    """Усі текстові поля матеріалів із підписом, де вони лежать."""
    out = []
    if isinstance(m.project, dict):
        out += [("project.json", str(m.project.get("name", ""))), ("project.json", str(m.project.get("goal", "")))]
    for r in m.log or []:
        if isinstance(r, dict):
            for key in ("request", "note"):
                out.append((f"ai_log.jsonl {r.get('id', '?')}.{key}", str(r.get(key, ""))))
    for s in m.stories or []:
        if isinstance(s, dict):
            out.append((f"stories.json {s.get('id', '?')}", str(s.get("text", ""))))
            for c in s.get("criteria", []) if isinstance(s.get("criteria"), list) else []:
                out.append((f"stories.json {s.get('id', '?')}", str(c.get("text", "") if isinstance(c, dict) else c)))
    for t in m.tests or []:
        if isinstance(t, dict):
            steps = t.get("steps") if isinstance(t.get("steps"), list) else []
            out.append((f"test_cases.json {t.get('id', '?')}", " ".join([str(t.get("title", "")), str(t.get("expected", ""))] + [str(x) for x in steps])))
    if isinstance(m.summary, dict):
        out.append(("summary.json", " ".join(str(x) for x in m.summary.get("lessons", []))))
    if m.conclusion:
        out.append(("conclusion.md", m.conclusion))
    return out


def rule_privacy(m):
    out = []
    for where, text in _texts(m):
        if EMAIL.search(text):
            out.append(f"{where}: знайдено адресу електронної пошти")
        for hit in PHONE.finditer(text):
            digits = re.sub(r"\D", "", hit.group())
            if re.fullmatch(r"380\d{9}|0\d{9}", digits):
                out.append(f"{where}: знайдено номер телефону")
                break
        for name, rx in SECRETS:
            if rx.search(text):
                out.append(f"{where}: знайдено секрет ({name})")
    return out


def log_problems(r, seen, today):
    if not isinstance(r, dict):
        return ["запис не є об'єктом"]
    p = [f"немає поля {f}" for f in LOG_FIELDS if f not in r]
    if "id" in r:
        if r["id"] in seen:
            p.append("повторний ідентифікатор")
        seen.add(r["id"])
    if "date" in r:
        d = parse_date(r["date"])
        if d is None:
            p.append("дата має вигляд РРРР-ММ-ДД")
        elif d.isoformat() > today:
            p.append("дата пізніша за сьогоднішню")
    if "stage" in r and r["stage"] not in STAGES:
        p.append(f"невідомий етап «{r['stage']}»")
    if "request" in r and words(r["request"]) < 5:
        p.append("запит коротший за 5 слів")
    if "data_class" in r:
        if r["data_class"] not in CLASSES:
            p.append(f"невідомий клас даних «{r['data_class']}»")
        elif r["data_class"] in ("персональні", "секретні"):
            p.append(f"заборонений клас даних «{r['data_class']}»")
    if "outcome" in r and r["outcome"] not in OUTCOMES:
        p.append(f"невідомий результат «{r['outcome']}»")
    num = lambda v: type(v) is int
    if "minutes_ai" in r and not (num(r["minutes_ai"]) and r["minutes_ai"] > 0):
        p.append("хвилини з ШІ мають бути додатними")
    if "minutes_manual_est" in r and not (num(r["minutes_manual_est"]) and r["minutes_manual_est"] >= 0):
        p.append("оцінка без ШІ не може бути від'ємною")
    for key in ("defects_caught", "defects_escaped"):
        if key in r and not (num(r[key]) and r[key] >= 0):
            p.append("лічильники дефектів мають бути невід'ємними")
            break
    if r.get("outcome") in ("правка", "відхилено") and "note" in r and words(r["note"]) < 4:
        p.append("потрібна нотатка про правку або причину (щонайменше 4 слова)")
    if r.get("outcome") == "прийнято" and num(r.get("defects_caught")) and r["defects_caught"] > 0:
        p.append("знайдено дефекти, але результат прийнято без змін")
    return p


def rule_log(m):
    if not m.log:
        return []
    out, seen = [], set()
    for k, r in enumerate(m.log, 1):
        label = r.get("id", f"#{k}") if isinstance(r, dict) else f"#{k}"
        out += [f"запис {label}: {x}" for x in log_problems(r, seen, m.today)]
    if len(m.log) < 8:
        out.append(f"у журналі {len(m.log)} записів, потрібно щонайменше 8")
    stages = [r.get("stage") for r in m.log if isinstance(r, dict)]
    for need in ("історії", "тести"):
        if stages.count(need) < 3:
            out.append(f"етап «{need}»: записів {stages.count(need)}, потрібно щонайменше 3")
    return out


def rule_review(m):
    if not m.log:
        return []
    rows = [r for r in m.log if isinstance(r, dict)]
    out = []
    changed = sum(1 for r in rows if r.get("outcome") in ("правка", "відхилено"))
    if changed < 2:
        out.append(f"правка або відхилення лише в {changed} записах: потрібно щонайменше 2 (інакше перевірки не видно)")
    caught = sum(r["defects_caught"] for r in rows if type(r.get("defects_caught")) is int)
    if caught < 2:
        out.append(f"перевірка знайшла лише {caught} дефектів у сумі, потрібно щонайменше 2")
    return out


def rule_links(m):
    if not (m.log and isinstance(m.stories, list) and isinstance(m.tests, list)):
        return []
    story_ids = {s.get("id") for s in m.stories if isinstance(s, dict)}
    test_ids = {t.get("id") for t in m.tests if isinstance(t, dict)}
    by_id = {r.get("id"): r for r in m.log if isinstance(r, dict)}
    out = []
    for r in by_id.values():
        refs = ids_of(r.get("artifact", ""))
        stage = r.get("stage")
        if not refs:
            out.append(f"запис {r.get('id')}: порожнє поле artifact (для етапів без артефакту поставте «-»)")
            continue
        if refs == ["-"]:
            if stage in ("історії", "критерії приймання", "тести"):
                out.append(f"запис {r.get('id')}: для етапу «{stage}» треба вказати ідентифікатори артефактів")
            continue
        pool = test_ids if stage == "тести" else story_ids if stage in ("історії", "критерії приймання") else story_ids | test_ids
        for ref in refs:
            if ref not in pool:
                out.append(f"запис {r.get('id')}: артефакту {ref} немає у відповідному файлі")
    for s in m.stories:
        if isinstance(s, dict):
            rec = by_id.get(s.get("source_log"))
            if rec is None:
                out.append(f"історія {s.get('id')}: source_log не вказує на запис журналу")
            elif s.get("id") not in ids_of(rec.get("artifact", "")):
                out.append(f"історія {s.get('id')}: запис {rec.get('id')} не згадує її в полі artifact")
    for t in m.tests:
        if isinstance(t, dict):
            rec = by_id.get(t.get("source_log"))
            if rec is None:
                out.append(f"тест-кейс {t.get('id')}: source_log не вказує на запис журналу")
            elif t.get("id") not in ids_of(rec.get("artifact", "")):
                out.append(f"тест-кейс {t.get('id')}: запис {rec.get('id')} не згадує його в полі artifact")
    return out


def _tokens(text):
    return set(re.findall(r"[а-яіїєґa-z']{4,}", text.lower()))


def rule_stories(m):
    s = m.stories
    if not isinstance(s, list):
        return []
    out = []
    if len(s) < 5:
        out.append(f"історій {len(s)}, потрібно щонайменше 5")
    roles = {str(r).strip().lower() for r in (m.project or {}).get("roles", [])} if isinstance(m.project, dict) else set()
    seen_ids, seen_texts = set(), set()
    for st in s:
        if not isinstance(st, dict):
            out.append("історія не є об'єктом")
            continue
        sid = st.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"S-\d+", sid):
            out.append(f"історія {sid}: ідентифікатор має вигляд S-1")
        if sid in seen_ids:
            out.append(f"історія {sid}: повторний ідентифікатор")
        seen_ids.add(sid)
        text = str(st.get("text", "")).strip()
        match = STORY.match(text)
        if not match:
            out.append(f"історія {sid}: текст має вигляд «Як <роль>, я хочу <мета>, щоб <цінність>.»")
        else:
            if roles and match["role"].strip().lower() not in roles:
                out.append(f"історія {sid}: роль «{match['role']}» відсутня у project.json")
            a, b = _tokens(match["goal"]), _tokens(match["why"])
            if a | b and len(a & b) / len(a | b) >= 0.5:
                out.append(f"історія {sid}: цінність повторює мету")
        if text in seen_texts:
            out.append(f"історія {sid}: дублює іншу історію")
        seen_texts.add(text)
        crit = st.get("criteria")
        if not isinstance(crit, list) or len(crit) < 2:
            out.append(f"історія {sid}: потрібно щонайменше 2 критерії приймання")
            continue
        for k, c in enumerate(crit, 1):
            if not isinstance(c, dict) or c.get("id") != f"{sid}.{k}":
                out.append(f"історія {sid}: критерій {k} має ідентифікатор {sid}.{k}")
            elif not GWT.match(str(c.get("text", "")).strip()):
                out.append(f"критерій {c.get('id')}: текст має вигляд «Дано ..., коли ..., тоді ....»")
    return out


def rule_tests(m):
    t = m.tests
    if not isinstance(t, list):
        return []
    out = []
    if len(t) < 8:
        out.append(f"тест-кейсів {len(t)}, потрібно щонайменше 8")
    crit_ids = []
    if isinstance(m.stories, list):
        for st in m.stories:
            if isinstance(st, dict) and isinstance(st.get("criteria"), list):
                crit_ids += [c.get("id") for c in st["criteria"] if isinstance(c, dict)]
    seen, titles, covered = set(), set(), set()
    negative = 0
    for tc in t:
        if not isinstance(tc, dict):
            out.append("тест-кейс не є об'єктом")
            continue
        tid = tc.get("id")
        if not isinstance(tid, str) or not re.fullmatch(r"TC-\d+", tid):
            out.append(f"тест-кейс {tid}: ідентифікатор має вигляд TC-1")
        if tid in seen:
            out.append(f"тест-кейс {tid}: повторний ідентифікатор")
        seen.add(tid)
        if tc.get("criterion") not in crit_ids:
            out.append(f"тест-кейс {tid}: критерій {tc.get('criterion')} відсутній у stories.json")
        covered.add(tc.get("criterion"))
        if tc.get("kind") not in ("позитивний", "негативний"):
            out.append(f"тест-кейс {tid}: kind має бути «позитивний» або «негативний»")
        negative += tc.get("kind") == "негативний"
        title = str(tc.get("title", "")).strip()
        if words(title) < 3:
            out.append(f"тест-кейс {tid}: назва щонайменше з трьох слів")
        if title.lower() in titles:
            out.append(f"тест-кейс {tid}: назва повторює іншу")
        titles.add(title.lower())
        steps = tc.get("steps")
        if not isinstance(steps, list) or len([x for x in steps if str(x).strip()]) < 2:
            out.append(f"тест-кейс {tid}: потрібно щонайменше 2 кроки")
        if words(tc.get("expected", "")) < 3:
            out.append(f"тест-кейс {tid}: очікуваний результат щонайменше з трьох слів")
    for cid in crit_ids:
        if cid not in covered:
            out.append(f"критерій {cid}: немає жодного тест-кейса")
    if negative < 2:
        out.append(f"негативних тест-кейсів {negative}, потрібно щонайменше 2")
    return out


def metrics(log):
    n = len(log)
    cnt = {o: sum(r["outcome"] == o for r in log) for o in OUTCOMES}
    manual = sum(r["minutes_manual_est"] for r in log)
    ai = sum(r["minutes_ai"] for r in log)
    return {"records": n,
            "accepted_pct": round(100 * cnt["прийнято"] / n, 1), "fixed_pct": round(100 * cnt["правка"] / n, 1),
            "rejected_pct": round(100 * cnt["відхилено"] / n, 1),
            "defects_caught": sum(r["defects_caught"] for r in log), "defects_escaped": sum(r["defects_escaped"] for r in log),
            "minutes_ai": ai, "minutes_manual_est": manual,
            "saved_pct": round(100 * (manual - ai) / manual, 1) if manual else None}


def rule_summary(m):
    s = m.summary
    if not isinstance(s, dict) or not m.log:
        return []
    for r in m.log:
        if not isinstance(r, dict) or any(f not in r for f in LOG_FIELDS) or r.get("outcome") not in OUTCOMES \
                or any(type(r.get(k)) is not int for k in ("minutes_ai", "minutes_manual_est", "defects_caught", "defects_escaped")):
            return ["summary.json: журнал має помилки форми, метрики не порівнюються (див. правило журналу)"]
    out = []
    for key, value in metrics(m.log).items():
        got = s.get(key, "немає")
        same = (got is None and value is None) or (isinstance(got, (int, float)) and not isinstance(got, bool)
                                                    and value is not None and abs(got - value) < 0.051)
        if not same:
            out.append(f"{key}: у summary.json {got}, за журналом {value}")
    lessons = s.get("lessons")
    if not isinstance(lessons, list) or len([x for x in lessons if words(x) >= 4]) < 3:
        out.append("lessons: щонайменше 3 висновки по 4 слова й більше")
    return out


def rule_conclusion(m):
    text = m.conclusion
    if not text:
        return []
    out = []
    heads = re.findall(r"^##\s+(.+?)\s*$", text, re.M)
    for h in HEADINGS:
        if h not in heads:
            out.append(f"conclusion.md: немає розділу «## {h}»")
    prose = re.sub(r"^#.*$", "", text, flags=re.M)
    if words(prose) < 150:
        out.append(f"conclusion.md: {words(prose)} слів, потрібно щонайменше 150")
    return out


RULES = [rule_files, rule_project, rule_privacy, rule_log, rule_review, rule_links, rule_stories, rule_tests,
         rule_summary, rule_conclusion]


def run_all(folder, today=None):
    m = Material(folder, today)
    return {rule.__name__: rule(m) for rule in RULES}
