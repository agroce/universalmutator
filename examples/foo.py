from __future__ import print_function

def myfunction(x):
    if (x < 6):
        print(x)
        x = 20
    while (x > 10):
        x -= 1
    return x

def main():
    y = 4
    v = myfunction(y)
    assert v==10

if __name__ == '__main__':
    main()
