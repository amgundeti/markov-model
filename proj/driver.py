import sys
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # TODO: add code here to open files & read text
    fileA = open(f"proj/{filenameA}", "r")
    fileB = open(f"proj/{filenameB}", "r")
    fileC = open(f"proj/{filenameC}", "r")

    # TODO: add code to call identify_speaker & print results
    
    #setting hastable boolean value for identify_speaker
    use_hash = False
    if hashtable_or_dict == "hashtable":
        use_hash = True
    
    actual = identify_speaker(fileA.read(), fileB.read(), fileC.read(), k, use_hash)

    logA, logB, speaker = actual

    #print sequence
    print("Speaker A:", logA)
    print("Speaker B:", logB)
    print(f"Conclusion: Speaker {speaker} most likely")

    fileA.close()
    fileB.close()
    fileC.close()


    # Output should resemble (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely
