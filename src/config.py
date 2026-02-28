from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

JOBS_CACHE = BASE_DIR / "data" / "jobs_cache.json"

EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"
TRANSLATION_MODEL = "Helsinki-NLP/opus-mt-ru-en"

DEFAULT_TOP_K = 6
FETCH_PER_QUERY = 50
MAX_PAGES_PER_QUERY = 2

# Skill level → (min_months, max_months)
SKILL_LEVEL_TIME = {
    "basic": (0.5, 1),
    "foundational": (1, 2),
    "intermediate": (2, 4),
    "advanced": (4, 7),
    "expert": (7, 12),
}

HH_API_BASE = "https://api.hh.ru"
HH_RUSSIA_AREA = "113"

# English career goal → Russian HH query keywords
EN_TO_RU_QUERIES = {
    "lawyer": ["юрист", "адвокат", "юрисконсульт"],
    "attorney": ["адвокат", "юрист"],
    "legal": ["юрист", "правовед", "юридический"],
    "python": ["python разработчик", "python developer"],
    "developer": ["разработчик", "developer", "программист"],
    "data analyst": ["аналитик данных", "data analyst"],
    "data scientist": ["data scientist", "специалист по данным"],
    "machine learning": ["machine learning", "ml инженер", "специалист ml"],
    "marketing": ["маркетолог", "специалист по маркетингу"],
    "smm": ["smm специалист", "контент менеджер"],
    "hr": ["hr менеджер", "менеджер по персоналу", "рекрутер"],
    "accountant": ["бухгалтер", "финансист"],
    "designer": ["дизайнер", "graphic designer"],
    "ux": ["ux дизайнер", "ui дизайнер", "продуктовый дизайнер"],
    "sales": ["менеджер по продажам", "sales manager"],
    "project manager": ["менеджер проектов", "project manager"],
    "product manager": ["продуктовый менеджер", "product manager"],
    "teacher": ["учитель", "преподаватель", "репетитор"],
    "doctor": ["врач", "медик"],
    "engineer": ["инженер"],
    "economist": ["экономист", "финансовый аналитик"],
    "journalist": ["журналист", "редактор", "корреспондент"],
    "psychologist": ["психолог"],
    "architect": ["архитектор"],
    "biologist": ["биолог"],
    "chemist": ["химик"],
    "pharmacist": ["фармацевт"],
    "nurse": ["медсестра", "медбрат"],
    "logistics": ["логист", "специалист по логистике"],
    "supply chain": ["логист", "менеджер цепочки поставок"],
    "finance": ["финансист", "финансовый менеджер", "аналитик"],
    "banking": ["банковский специалист", "кредитный специалист"],
    "analyst": ["аналитик", "бизнес аналитик"],
    "backend": ["backend разработчик", "серверный разработчик"],
    "frontend": ["frontend разработчик", "веб разработчик"],
    "fullstack": ["fullstack разработчик"],
    "devops": ["devops инженер", "системный администратор"],
    "cybersecurity": ["специалист по безопасности", "информационная безопасность"],
    "java": ["java разработчик"],
    "javascript": ["javascript разработчик", "js разработчик"],
    "react": ["react разработчик", "frontend разработчик"],
    "ios": ["ios разработчик", "swift разработчик"],
    "android": ["android разработчик", "kotlin разработчик"],
    "qa": ["qa инженер", "тестировщик", "качество"],
    "tester": ["тестировщик", "qa специалист"],
    "business analyst": ["бизнес аналитик", "системный аналитик"],
    "copywriter": ["копирайтер", "контент менеджер"],
    "translator": ["переводчик"],
    "sociologist": ["социолог"],
    "political": ["политолог", "политический аналитик"],
}

# HH.ru area IDs for city filtering
CITY_AREA_IDS = {
    "Any city": None,
    "Москва": "1",
    "Санкт-Петербург": "2",
    "Новосибирск": "4",
    "Екатеринбург": "3",
    "Казань": "88",
    "Нижний Новгород": "66",
    "Челябинск": "104",
    "Самара": "78",
    "Омск": "68",
    "Ростов-на-Дону": "76",
    "Уфа": "99",
    "Красноярск": "54",
    "Воронеж": "26",
    "Пермь": "72",
    "Волгоград": "24",
    "Краснодар": "53",
    "Тюмень": "97",
    "Саратов": "79",
    "Тольятти": "92",
    "Ижевск": "36",
    "Барнаул": "10",
    "Иркутск": "35",
    "Хабаровск": "101",
    "Владивосток": "22",
    "Минск": "1002",
    "Алматы": "160",
    "Ташкент": "2759",
}

# Noise words to filter from skill extraction (soft skills, filler phrases)
SKILL_NOISE_WORDS = {
    # Russian soft-skill / filler
    "ответственность", "стрессоустойчивость", "коммуникабельность",
    "пунктуальность", "внимательность", "исполнительность",
    "инициативность", "целеустремленность", "дисциплинированность",
    "обучаемость", "работоспособность", "многозадачность",
    "грамотная речь", "грамотная устная и письменная речь",
    "желание развиваться", "умение работать в команде",
    "нацеленность на результат", "аналитический склад ума",
    "высшее образование", "опыт работы", "без вредных привычек",
    # English soft-skill / filler
    "responsibility", "stress resistance", "communication skills",
    "team player", "attention to detail", "self-motivated",
    "fast learner", "hard working", "proactive", "multitasking",
    "good communication", "problem solving", "critical thinking",
    "time management", "leadership", "work ethic",
    "higher education", "work experience", "degree required",
}
