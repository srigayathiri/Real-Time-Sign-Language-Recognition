# Dictionary to map English words to Tamil
english_to_tamil = {

    'callme': 'என்னை அழைக்கவும்',
    'first': 'முதல்',
    'livelong': 'நீண்ட வாழ்க்கை வாழ',
    'okay': 'சரி',
    'peace': 'சமாதானம்',
    'rock': 'ராக்',
    'smile': 'சிரிக்க',
    'stop': 'நிறுத்தம்',
    'thumbsdown': 'தும்பு கீழே',
    'thumbsup': 'தும்பு மேலே'
    # Add more mappings here as needed
}

def translate_to_tamil(input_text):
    # Split the input text into words
    words = input_text.lower().split()

    # Translate each word to Tamil
    tamil_words = []
    for word in words:
        tamil_word = english_to_tamil.get(word)
        if tamil_word:
            tamil_words.append(tamil_word)
        else:
            tamil_words.append(word)

    # Join the Tamil words to form the translated text
    tamil_text = ' '.join(tamil_words)

    return tamil_text


