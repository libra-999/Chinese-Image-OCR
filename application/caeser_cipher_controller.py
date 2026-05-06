import string
from fastapi import FastAPI , HTTPException

app = FastAPI()
lower_word = string.ascii_lowercase # Get letter lowercase
upper_word = string.ascii_uppercase # Get letter uppercase
number = string.digits # Get number
symbols = string.punctuation # Get symbols
total_letter = 26
total_symbol = 32
total_dgit = 10

@app.post("/convert/caeser-cipher")
async def convert_to_caeser_cipher(text , shift_number : int):
    try :
        caeser_value_new = list(text)
        result = ""
        for new_text in caeser_value_new:
            if new_text == " ":
                result += " "
            elif new_text in symbols:
                index = symbols.index(new_text)
                new_text = (index + shift_number ) % total_symbol
                result += symbols[new_text]
            elif new_text in number:
                index = number.index(new_text)
                new_text = (index + shift_number) % total_dgit
                result += number[new_text]
            elif new_text in lower_word:
                index = lower_word.index(new_text)
                new_text = (index + shift_number) % total_letter
                result += lower_word[new_text]
            elif new_text in upper_word:
                index =upper_word.index(new_text)
                new_text = (index + shift_number) % total_letter
                result += upper_word[new_text]
            else:
                result += new_text
        return {
            "Convert to Caeser Cipher": result
        }
    except Exception as e:
        raise HTTPException(500, f"You get wrong letter english, message : {str(e)} ")
    
@app.post("/convert/normal-word")
async def from_caeser_cipher_to_text(caeser_cipher, shift_number : int):
    try :
        caeser_value_new = list(caeser_cipher)
        result = ""
        for new_text in caeser_value_new:
            if new_text == " ":
                result += " "
            elif new_text in symbols:
                index = symbols.index(new_text)
                new_text = (index - shift_number ) % total_symbol
                result += symbols[new_text]
            elif new_text in number:
                index = number.index(new_text)
                new_text = (index - shift_number) % total_dgit # 10 dgit
                result += number[new_text]
            elif new_text in lower_word:
                index = lower_word.index(new_text)
                new_text = (index - shift_number) % total_letter
                result += lower_word[new_text]
            elif new_text in upper_word:
                index =upper_word.index(new_text)
                new_text = (index - shift_number) % total_letter
                result += upper_word[new_text]
            else:
                result += new_text
        
        return {
            "Normal text": result
        }
    except Exception as e:
        raise HTTPException(500,  f"You get wrong letter english, message : {str(e)} ")

