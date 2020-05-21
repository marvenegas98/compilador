import basic
print('you tried')
while True:
    text = input('basic > ')
    result, error = basic.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)
