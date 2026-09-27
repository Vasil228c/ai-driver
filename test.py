from ai import aidriver


aig = aidriver()

while True:
    aig.send_msg(input("> "))
    
    for n in aig.get_stream_answer():
        print(n, flush=True, end="")
    print()