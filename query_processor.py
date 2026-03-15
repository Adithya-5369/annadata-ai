CATEGORIES = {
    "disease": ["disease", "rust", "blight", "fungus", "infection",
                "yellow", "spots", "leaves", "dying", "रोग", "బాధ", "ರೋಗ"],
    "pest": ["pest", "insect", "aphid", "worm", "larvae", "bug",
             "कीड़े", "పురుగు", "ಕೀಟ"],
    "fertilizer": ["fertilizer", "nutrient", "nitrogen", "urea", "manure",
                   "खाद", "ఎరువు", "ಗೊಬ್ಬರ"],
    "weather": ["weather", "rain", "drought", "flood", "temperature",
                "मौसम", "వాతావరణం", "ಹವಾಮಾನ"],
    "scheme": ["scheme", "subsidy", "government", "kisan", "yojana",
               "योजना", "పథకం", "ಯೋಜನೆ"],
    "crop": ["crop", "sow", "harvest", "season", "plant", "grow",
             "फसल", "పంట", "ಬೆಳೆ"],
    "soil": ["soil", "pH", "health", "test", "मिट्टी", "నేల", "ಮಣ್ಣು"],
}

CATEGORY_INSTRUCTIONS = {
    "disease": "Focus on disease symptoms, causes, and treatment methods.",
    "pest": "Focus on pest identification and integrated pest management.",
    "fertilizer": "Focus on specific fertilizer quantities and application methods.",
    "weather": "Focus on weather impact on crops and preventive measures.",
    "scheme": "Focus on eligibility, benefits, and how to apply for the scheme.",
    "crop": "Focus on crop cultivation practices and best seasons.",
    "soil": "Focus on soil health improvement and testing methods.",
    "general": "Provide comprehensive farming advice.",
}

def classify_query(query_english):
    query_lower = query_english.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in query_lower:
                return category
    return "general"

def build_prompt(query, context, category):
    instruction = CATEGORY_INSTRUCTIONS.get(category, CATEGORY_INSTRUCTIONS["general"])
    return f"""You are Annadata AI, an expert agricultural advisor for Indian farmers.
{instruction}
Use the context from ICAR documents below to give practical, specific advice.
If context is insufficient, use your general agricultural knowledge.

Context from ICAR documents:
{context}

Farmer's Question: {query}

Provide a detailed, practical answer:"""