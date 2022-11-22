def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
            yield value

def call_find_by_key(data, target):

    y = []

    for x in find_by_key(data, target):
        y.append(x) 
    
    return x



if __name__ == '__main__':

    data = {
  "key_1": {
    "name": "Alice",
    "age": 21
  },
  "key_2": {
    "name": "Bob",
    "hobbies": ["cryptography", "tennis"]
  }
}

    x = call_find_by_key(data,"name")

    print(x)

