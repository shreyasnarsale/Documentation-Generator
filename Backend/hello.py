print("Hello from Python")
try:
    with open("hello_output.txt", "w") as f:
        f.write("Hello from Python File Write")
    print("File written.")
except Exception as e:
    print(f"Error: {e}")
