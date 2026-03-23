"""
Krishi Sathi - Intent Classifier
Supports: Bengali, Hindi, English
Intents: IRRIGATION, PESTICIDE_SPRAY, CROP_RECOMMENDATION,
         HARVEST, FERTILIZER, WEATHER, CROP_CARE, OUT_OF_SCOPE
"""

class KrishiIntentClassifier:

    def classify(self, query):
        query = query.strip().lower()

        # ══════════════════════════════════════════
        # BENGALI (বাংলা)
        # ══════════════════════════════════════════

        # -- Irrigation (সেচ / পানি) --
        if any(w in query for w in [
            'পানি', 'জল', 'সেচ', 'সেচন', 'সেচের', 'জলসেচ',
            'ড্রিপ', 'স্প্রিংকলার', 'পানির'
        ]):
            return {'intent': 'IRRIGATION', 'confidence': 0.99, 'language': 'bn'}

        # -- Pesticide / Spray (কীটনাশক / স্প্রে) --
        if any(w in query for w in [
            'স্প্রে', 'কীটনাশক', 'বালাইনাশক', 'কীটপতঙ্গ',
            'পোকা', 'পোকামাকড়', 'ছত্রাক', 'রোগ', 'ওষুধ',
            'দাওয়াই', 'ছিটানো', 'স্প্রে করা'
        ]):
            return {'intent': 'PESTICIDE_SPRAY', 'confidence': 0.99, 'language': 'bn'}

        # -- Fertilizer (সার) --
        if any(w in query for w in [
            'সার', 'ইউরিয়া', 'পটাশ', 'ফসফেট', 'ড্যাপ',
            'জৈব সার', 'রাসায়নিক সার', 'কম্পোস্ট', 'সার দেওয়া'
        ]):
            return {'intent': 'FERTILIZER', 'confidence': 0.99, 'language': 'bn'}

        # -- Harvest (কাটাই / ফসল তোলা) --
        if any(w in query for w in [
            'কাটা', 'কাটাই', 'ফসল তোলা', 'মাড়াই', 'ধান কাটা',
            'কখন কাটব', 'পাকা', 'পেকেছে'
        ]):
            return {'intent': 'HARVEST', 'confidence': 0.99, 'language': 'bn'}

        # -- Weather (আবহাওয়া) --
        if any(w in query for w in [
            'আবহাওয়া', 'বৃষ্টি', 'রোদ', 'তাপমাত্রা', 'ঝড়',
            'বন্যা', 'খরা', 'শিলাবৃষ্টি', 'মেঘ'
        ]):
            return {'intent': 'WEATHER', 'confidence': 0.99, 'language': 'bn'}

        # -- Crop Recommendation (ফসল পরামর্শ) --
        if any(w in query for w in [
            'ফসল', 'ধান', 'গম', 'ভুট্টা', 'পাট', 'আলু',
            'পেঁয়াজ', 'রসুন', 'সবজি', 'ডাল', 'তুলা',
            'লাগাব', 'বুনব', 'চাষ', 'চাষাবাদ', 'কোন ফসল',
            'কি ফসল', 'কী ফসল', 'মরিচ', 'টমেটো', 'বেগুন',
            'শসা', 'করলা', 'লাউ', 'কুমড়া'
        ]):
            return {'intent': 'CROP_RECOMMENDATION', 'confidence': 0.99, 'language': 'bn'}

        # -- Crop Care (পরিচর্যা) --
        if any(w in query for w in [
            'পরিচর্যা', 'যত্ন', 'গাছ মরে', 'পাতা হলুদ',
            'ফলন কম', 'বৃদ্ধি', 'চারা'
        ]):
            return {'intent': 'CROP_CARE', 'confidence': 0.99, 'language': 'bn'}

        # ══════════════════════════════════════════
        # HINDI (हिंदी)
        # ══════════════════════════════════════════

        # -- Irrigation --
        if any(w in query for w in [
            'पानी', 'सिंचाई', 'ड्रिप', 'नहर', 'नमी'
        ]):
            return {'intent': 'IRRIGATION', 'confidence': 0.99, 'language': 'hi'}

        # -- Pesticide / Spray --
        if any(w in query for w in [
            'स्प्रे', 'कीटनाशक', 'दवाई', 'दवा', 'कीड़े',
            'रोग', 'फफूंद', 'छिड़काव'
        ]):
            return {'intent': 'PESTICIDE_SPRAY', 'confidence': 0.99, 'language': 'hi'}

        # -- Fertilizer --
        if any(w in query for w in [
            'खाद', 'उर्वरक', 'यूरिया', 'डीएपी', 'पोटाश', 'खाद डालना'
        ]):
            return {'intent': 'FERTILIZER', 'confidence': 0.99, 'language': 'hi'}

        # -- Harvest --
        if any(w in query for w in [
            'कटाई', 'फसल काटना', 'कब काटें', 'पकी', 'तैयार'
        ]):
            return {'intent': 'HARVEST', 'confidence': 0.99, 'language': 'hi'}

        # -- Weather --
        if any(w in query for w in [
            'मौसम', 'बारिश', 'तापमान', 'धूप', 'सूखा', 'बाढ़'
        ]):
            return {'intent': 'WEATHER', 'confidence': 0.99, 'language': 'hi'}

        # -- Crop Recommendation --
        if any(w in query for w in [
            'फसल', 'धान', 'गेहूं', 'मक्का', 'सब्जी', 'आलू',
            'प्याज', 'लहसुन', 'कपास', 'दाल', 'कौनसी फसल',
            'कौन सी फसल', 'क्या बोयें', 'बुवाई'
        ]):
            return {'intent': 'CROP_RECOMMENDATION', 'confidence': 0.99, 'language': 'hi'}

        # -- Crop Care --
        if any(w in query for w in [
            'देखभाल', 'पत्ते पीले', 'पौधा मर', 'उपज कम', 'पनीरी'
        ]):
            return {'intent': 'CROP_CARE', 'confidence': 0.99, 'language': 'hi'}

        # ══════════════════════════════════════════
        # ENGLISH
        # ══════════════════════════════════════════

        # -- Irrigation --
        if any(w in query for w in [
            'water', 'irrigation', 'irrigate', 'drip', 'moisture',
            'watering', 'canal', 'sprinkler'
        ]):
            return {'intent': 'IRRIGATION', 'confidence': 0.95, 'language': 'en'}

        # -- Pesticide / Spray --
        if any(w in query for w in [
            'spray', 'pesticide', 'insecticide', 'fungicide',
            'pest', 'disease', 'bug', 'insects', 'spraying'
        ]):
            return {'intent': 'PESTICIDE_SPRAY', 'confidence': 0.95, 'language': 'en'}

        # -- Fertilizer --
        if any(w in query for w in [
            'fertilizer', 'urea', 'npk', 'dap', 'potash',
            'compost', 'manure', 'nutrient'
        ]):
            return {'intent': 'FERTILIZER', 'confidence': 0.95, 'language': 'en'}

        # -- Harvest --
        if any(w in query for w in [
            'harvest', 'harvesting', 'reap', 'cut crop',
            'when to cut', 'ripe', 'ready to harvest'
        ]):
            return {'intent': 'HARVEST', 'confidence': 0.95, 'language': 'en'}

        # -- Weather --
        if any(w in query for w in [
            'weather', 'rain', 'temperature', 'humidity',
            'drought', 'flood', 'storm', 'sunshine'
        ]):
            return {'intent': 'WEATHER', 'confidence': 0.95, 'language': 'en'}

        # -- Crop Recommendation --
        if any(w in query for w in [
            'crop', 'plant', 'grow', 'sow', 'seed', 'farming',
            'cultivate', 'which crop', 'what crop', 'paddy',
            'wheat', 'maize', 'vegetable', 'rice'
        ]):
            return {'intent': 'CROP_RECOMMENDATION', 'confidence': 0.95, 'language': 'en'}

        # -- Crop Care --
        if any(w in query for w in [
            'yellow leaves', 'dying', 'low yield', 'seedling',
            'care', 'growth', 'wilting'
        ]):
            return {'intent': 'CROP_CARE', 'confidence': 0.95, 'language': 'en'}

        # ══════════════════════════════════════════
        # OUT OF SCOPE (default)
        # ══════════════════════════════════════════
        return {'intent': 'OUT_OF_SCOPE', 'confidence': 1.0, 'language': 'unknown'}


classifier = KrishiIntentClassifier()
