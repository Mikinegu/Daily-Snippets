def wordBreak(s, wordDict):
    word_set = set(wordDict)
    memo = {}

    def backtrack(start):
        if start == len(s):
            return [""]

        if start in memo:
            return memo[start]

        result = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                subsentences = backtrack(end)
                for sub in subsentences:
                    if sub:
                        result.append(word + " " + sub)
                    else:
                        result.append(word)

        memo[start] = result
        return result

    return backtrack(0)

s = "catsanddog"
wordDict = ["cat", "cats", "and", "sand", "dog"]
print(wordBreak(s, wordDict))
