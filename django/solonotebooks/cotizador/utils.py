def stringCompare(comp1, comp2):
    comp1_words = comp1.lower().split()
    comp2_words = comp2.lower().split()
    counter = 0;
    for word in comp2_words:
        for comp1_word in comp1_words:
            if word in comp1_word:
                counter += 1;
            
    return 100.0 * counter / len(comp2_words)
