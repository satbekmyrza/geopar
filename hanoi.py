count = 0


def tell_move(peg, source, destination):
    print('moving', peg, 'from', source, 'to', destination)


def run(n, source, spare, destination):
    global count
    count += 1
    if n == 1:
        tell_move(1, source, destination)
    else:
        run(n - 1, source, destination, spare)
        tell_move(n, source, destination)
        run(n - 1, spare, source, destination)


run(4, '.H', '.F', '.D')
print('total steps:', count)
