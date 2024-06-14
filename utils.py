''' 
Цей файл містить допоміжну функцію handle_response, яка обробляє відповіді від API, перевіряючи статус коду і повертаючи JSON-дані.    
'''   
async def handle_response(response):
    if response.status != 200:
        raise Exception(f"API request failed with status code {response.status}")
    return await response.json()