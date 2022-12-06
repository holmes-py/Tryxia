
def uniqueSubdomains(listOfSubdFiles, targetName):
    '''
    Function to read all the files in listOfSubdomainFiles list and create a list of unique subdomains.
    '''
    with open(f'unique_subdomains-{targetName}.txt', 'w+') as f:
        for file in listOfSubdFiles:
            with open(file, 'r') as subf:
                for line in subf:
                    print(line)
                    input()
                    subdomain = line.strip()
                    if subdomain not in f:
                        f.write(subdomain + '\n')


uniqueSubdomains(['amass_output-restream.io.txt', 'subfinder_output-restream.io.txt'], 'test')