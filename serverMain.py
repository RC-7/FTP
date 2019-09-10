from serverPi import serverPi

def main():
    sp = serverPi()
    sp.listen()

if __name__ == "__main__":
    main()