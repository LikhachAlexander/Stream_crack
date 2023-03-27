from string import ascii_uppercase, ascii_lowercase
from random import choice, randrange

from tqdm import tqdm


from ngram import NGram


def decode(s, key):
    return [c1 ^ c2 for c1, c2 in zip(s, key)]


# key_c = [231, 140, 199, 10, 30, 100, 165, 124, 1, 210, 249, 124, 86, 208, 78, 221, 97, 126, 82, 184, 63, 229, 211, 66, 166, 66, 47, 58, 236, 53, 97, 214, 45, 237, 7, 53, 90, 84, 125, 126, 51, 129, 219, 21]
# https://www.youtube.com/watch?v=Jc8VaMQ5aOo
def get_data(data_file, n_samples, max_n, space_thres):

    with open(data_file, 'r', encoding='UTF-8') as file:
        samples = [bytes.fromhex(file.readline().strip('\r\n'))
                   for i in range(n_samples)]
        cipher = bytes.fromhex(file.readline().strip('\r\n'))

        # finding probable spaces
        # i - char index, k - sample index
        key = [0] * len(samples[0])
        for i in range(len(samples[0])):
            for k in range(len(samples)):
                # find sums of current chars
                space_score = 0
                for k1 in range(len(samples)):
                    if k1 == k:
                        continue
                    # find k + k1 char result
                    sum_xor = samples[k][i] ^ samples[k1][i]
                    if chr(sum_xor) in (ascii_uppercase + ascii_lowercase):
                        space_score += 1
                if space_score > space_thres:
                    # decode key
                    key[i] = samples[k][i] ^ ord(' ')

        # probable key values
        alphabet = ascii_lowercase + ascii_uppercase + "0123456789" + " .,;"
        probable_key = [[] for _i in range(len(key))]

        for i in range(len(key)):
            if key[i] != 0:
                probable_key[i].append(key[i])
                continue

            for j in range(256):
                score = 0
                for k in range(len(samples)):
                    sum_xor = j ^ samples[k][i]
                    if chr(sum_xor) in alphabet:
                        score += 1
                if score == len(samples):
                    probable_key[i].append(j)
            if len(probable_key[i]) == 0:
                probable_key[i] = list(range(256))
        
        total = 1
        for k in probable_key:
            total *= len(k)
        print("Possible combinations:", total)

        l = len(samples)

        ng = NGram('english_quadgrams.txt')
        fit = -1000000

        # random guess
        fit = -1000000
        n = 0
        key = [l[0] for l in probable_key]
        print("Guessing")
        t = tqdm(total=max_n)
        best_key = None
        while fit < -10:
            # pick random index
            k = key[:]
            x = randrange(l)
            # print(x)
            if len(probable_key[x]) == 1:
                continue
            n += 1
            t.update(1)
            # try all probable key[index] values
            is_changed = False
            current_highest = -100
            highest_i = -1
            for i in range(len(probable_key[x])):
                k[x] = probable_key[x][i]
                # decode text
                text = ""
                for j in range(len(samples)):
                    d = decode(samples[j], k)
                    text += "".join([chr(c) for c in d if chr(c)
                                    in (ascii_lowercase + ascii_uppercase)])
                # print(text)

                F = ng.fitness(text.upper())
                # print(F)
                if F > current_highest:
                    current_highest = F
                    highest_i = i
                if F > fit:
                    key = k[:]
                    fit = F
                    # print("New key", key)
                    print("\n   Fitness =", fit)
                    best_key = key[:]
                    t.reset()
                    n = 0
                    is_changed = True

            if not is_changed:
                # k[x] = choice(probable_key[x])
                k[x] = probable_key[x][highest_i]
                key = k[:]

            if n > max_n:
                print("\nMax_n quit")
                break
                
        t.close()
        print("Done!")
        key = best_key

        data = {
            "samples": samples,
            "cipher": cipher,
            "key": key,
            "probable_key": probable_key
        }
        return data
