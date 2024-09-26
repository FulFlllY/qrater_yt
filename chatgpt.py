from openai import OpenAI


keywords = [
    "Joyful", "Energizing", "Feel-good", "Uplifting", "Euphoric", "Melancholic",
    "Sorrowful", "Gloomy", "Tearful", "Aggressive", "Furious",
    "Explosive", "Relaxing", "Meditative",
    "Chilling", "Foreboding", "Tense", "Romantic", "Heartfelt", "Amorous", "Sentimental", "Nostalgic", "Empowering", "Inspiring",
    "Captivating", "Hypnotic", "Transfixing"
]


def get_gpt_result(song_name, song_comments):
    comments_content = " ".join(song_comments)
    prompt = f"Classify the emotional impact of this song: {song_name}. Based on the following comments: {comments_content}. Use predefined keywords to determine the dominant emotional responses. Don't try to squeeze in redundant stuffs but just put keywords that are most clear and essential. Maybe 3 to 4?) Keywords include: {', '.join(keywords)}."
    #', '.join(keywords)}. ','로 떨어져있는 애들 붙이기
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    result = []
    sentence = ""
    for chunk in stream:
        text = chunk.choices[0].delta.content

        if text:
            sentence += text
    words = sentence.split()

    for word in words :
        # print (word)
        found_keywords = [keyword for keyword in keywords if keyword.lower() in word.lower()]
        result.extend(found_keywords)
    return result
