def main():
    base = []
    mode = True
    with open('data.txt') as f:
        for line in f.readlines():
            line = line.strip()
            if '*' in line:
                mode = False
                continue
                
            if mode:
                base.append(line)
            else:
                if line not in base:
                    print line
            

                
if __name__ == '__main__':
    main()
    
