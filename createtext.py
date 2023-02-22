import random

# Hàm đọc dữ liệu từ file
def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
					data = f.read()
					return data
  
# Hàm tạo model Markov Chain
def build_model(data, order):
    model = {}
    for i in range(len(data)-order):
        state = data[i:i+order]
        next_state = data[i+order]
        if state in model:
            model[state].append(next_state)
        else:
            model[state] = [next_state]
    return model

# Hàm sinh văn bản mới từ model
def generate_text(model, length, order):
    start = random.choice(list(model.keys()))
    state = start
    output = start
    for i in range(length-order):
        if state in model:
            next_state = random.choice(model[state])
            output += next_state
            state = output[-order:]
        else:
            break
    return output

# Đọc dữ liệu từ file
data = read_data('gutenberg.txt') # Nguồn https://www.gutenberg.org/files/100/100-0.txt

# Xây dựng model
order = 5
model = build_model(data, order)

# Sinh văn bản mới
length = 100
text = generate_text(model, length, order)

# Hiển thị văn bản mới vào file output.txt
with open('new-text.txt', 'w', encoding='utf-8') as f:
	f.write(text)

print('Done!, check new-text.txt')