from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    msg = ""
    sums = 0
    try:
        sums = sumOfTwo("a", 6)
        return f"Hello world {sums}"
    except Exception as e:
        msg = f"Произошла ошибка: {e}"
        return msg
    finally:
        return f"Вот сумма: {sums}" if sums != 0 else msg
        


def sumOfTwo(a: int | float, b: int | float) -> int | float:
    return a + b