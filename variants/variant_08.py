from datetime import datetime

def check_log(records: list, today: str) -> dict:
    # 1. Перевірка дати перевірки
    try:
        datetime.strptime(today, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Дата перевірки має вигляд РРРР-ММ-ДД")
    
    # 2. Перевірка журналу на порожнечу
    if not records:
        raise ValueError("Журнал порожній")
        
    required_fields = [
        "id", "date", "stage", "tool", "request", 
        "data_class", "outcome", "minutes_ai", 
        "minutes_manual_est", "defects_caught", 
        "defects_escaped", "note"
    ]
    
    stages = ["історії", "критерії приймання", "тести", "оцінки", "код", "рев'ю", "дослідження відгуків"]
    data_classes = ["вигадані", "публічні", "власні", "персональні", "секретні"]
    outcomes = ["прийнято", "правка", "відхилено"]
    
    seen_ids = set()
    rows = []
    ok_count = 0
    bad_count = 0
    
    for idx, rec in enumerate(records, start=1):
        if not isinstance(rec, dict):
            raise ValueError(f"Запис {idx} не є словником")
            
        rec_id = rec.get("id", f"#{idx}")
        problems = []
        
        # Перевірка наявності обов'язкових полів (по порядку)
        for field in required_fields:
            if field not in rec:
                problems.append(f"немає поля {field}")
                
        # Якщо немає поля id, або воно вже було
        if "id" in rec:
            if rec["id"] in seen_ids:
                problems.append("повторний ідентифікатор")
            else:
                seen_ids.add(rec["id"])
                
        # Перевірка дати запису
        date_str = rec.get("date")
        date_valid = False
        if isinstance(date_str, str):
            try:
                rec_date = datetime.strptime(date_str, "%Y-%m-%d")
                date_valid = True
            except ValueError:
                pass
                
        if "date" in rec:
            if not date_valid:
                problems.append("дата має вигляд РРРР-ММ-ДД")
            else:
                try:
                    if rec_date > datetime.strptime(today, "%Y-%m-%d"):
                        problems.append("дата пізніша за дату перевірки")
                except ValueError:
                    pass
                    
        # Перевірка етапу
        stage = rec.get("stage")
        if "stage" in rec and stage not in stages:
            problems.append(f"невідомий етап «{stage}»")
            
        # Перевірка запиту (коротший за 5 слів)
        request_val = rec.get("request")
        if "request" in rec and isinstance(request_val, str):
            words = request_val.strip().split()
            if len(words) < 5:
                problems.append("запит коротший за 5 слів")
                
        # Перевірка класу даних
        d_class = rec.get("data_class")
        if "data_class" in rec:
            if d_class not in data_classes:
                problems.append(f"невідомий клас даних «{d_class}»")
            elif d_class in ["персональні", "секретні"]:
                problems.append(f"заборонений клас даних «{d_class}»")
                
        # Перевірка результату (outcome)
        outcome = rec.get("outcome")
        if "outcome" in rec and outcome not in outcomes:
            problems.append(f"невідомий результат «{outcome}»")
            
        # Перевірка хвилин з ШІ (мають бути додатним цілим числом, логічні не допускаються)
        min_ai = rec.get("minutes_ai")
        if "minutes_ai" in rec:
            if isinstance(min_ai, bool) or not isinstance(min_ai, int) or min_ai <= 0:
                problems.append("хвилини з ШІ мають бути додатними")
                
        # Перевірка часу без ШІ (не може бути від'ємною, логічні не допускаються)
        min_manual = rec.get("minutes_manual_est")
        if "minutes_manual_est" in rec:
            if isinstance(min_manual, bool) or not isinstance(min_manual, (int, float)) or min_manual < 0:
                problems.append("оцінка без ШІ не може бути від'ємною")
                
        # Перевірка лічильників дефектів
        def_caught = rec.get("defects_caught")
        def_escaped = rec.get("defects_escaped")
        
        counters_valid = True
        for dc in [def_caught, def_escaped]:
            if isinstance(dc, bool) or not isinstance(dc, int) or dc < 0:
                counters_valid = False
                
        if "defects_caught" in rec or "defects_escaped" in rec:
            if not counters_valid:
                problems.append("лічильники дефектів мають бути невід'ємними")
                
        # Перевірка нотатки для правки або відхилення (щонайменше 4 слова)
        note = rec.get("note", "")
        if outcome in ["правка", "відхилено"]:
            note_words = str(note).strip().split() if note else []
            if len(note_words) < 4:
                problems.append("потрібна нотатка про правку або причину")
                
        # Знайдено дефекти, але результат прийнято без змін
        if outcome == "прийнято" and isinstance(def_caught, int) and def_caught > 0:
            problems.append("знайдено дефекти, але результат прийнято без змін")
            
        # Унікалізуємо проблеми, зберігаючи порядок першої появи за правилами
        # Але оскільки перевірки йдуть чітко по порядку, дублікатів зазвичай не виникає
        
        if problems:
            bad_count += 1
            rows.append({"id": rec_id, "problems": problems})
        else:
            ok_count += 1
            rows.append({"id": rec_id, "problems": []})
            
    complete = (bad_count == 0)
    
    return {
        "rows": rows,
        "ok": ok_count,
        "bad": bad_count,
        "complete": complete
    }