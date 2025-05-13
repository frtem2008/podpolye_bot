
def word_in_mes(word: str, mes: str) -> bool:
    mes = mes.lower()
    word = word.lower()

    if word in mes:
        return True
    return False