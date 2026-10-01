# Stack: last in, first out (like a pile of plates)
# A plain list works: append puts on top, pop takes from the top, both fast

stack = []
stack.append("a")
stack.append("b")
stack.append("c")  # ["a", "b", "c"], the top is the right-hand end
top_item = stack[-1]  # "c", look without removing

while stack:  # an empty list counts as False
    top_item = stack.pop()  # "c", then "b", then "a"

# Example: checking that brackets are balanced
def brackets_balanced(text):
    matching_open = {")": "(", "]": "[", "}": "{"}
    open_brackets = []
    for character in text:
        if character in "([{":
            open_brackets.append(character)
        elif character in ")]}":
            if not open_brackets or open_brackets.pop() != matching_open[character]:
                return False
    return not open_brackets  # anything left open means unbalanced

balanced = brackets_balanced("(a[b]{c})")  # True
unbalanced = brackets_balanced("(a[b)]")  # False
