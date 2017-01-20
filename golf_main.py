def main():
    """
    The Wake Golf Tour association has their tournament information
    saved in four csv files.  This information is to be rearranged
    and statistics calculated and stored in eight new csv files.
    Later this information will be placed in a SQLite database.

    Read in these csv input files:

       1. golf course info from "golfCoursesInput.csv"
          15 records in this format:
          course_name, par_h1, par_h2, ..., par_h18

       2. golfers info from "golfersInput.csv"
          30 records in this format:
          golfer_name

       3. tournaments info from "tournamentsInput.csv"
          15 sets of records in this format:
          course_name, tourn_name, start_date, num_rounds, num_golfers
          golfer1
          golfer2
          ...
          golfer15

       4. round scores info from "roundScoresInput.csv"
          675 records in this format:
          golfer_name tourn_name, day, hole1, hole2, ..., hole18

    Write out the reorganized information into these csv output files:

        1. golf course info into "golfCourses.csv"
           5 records in this format:
           course_id, name, total_par, par_h1, par_h2, ..., par_h18

        2. holes info into "holes.csv"
           90 records in this format:
           hole_id, course_id, num, par

        3. golfer info into "golfers.csv"
           30 records in this format:
           golfer_id, name

        4. tournaments info into "tournaments.csv"
           15 records in this format:
           tourn_id, tourn_name, course_id, start_date, num_rounds,
           num_golfers, golferID1, golferID2, ..., golferID15

        5. rounds info into "rounds.csv"
           45 records in this format:
           round_id, tourn_id, day

        6. golfer round scores info into "golferRoundScores.csv"
           675 records in this format:
           golfer_round_id, tourn_id, round_id, golfer_id,
           total_round_score, hole1_score, hole2_score, ..., hole18_score

        7. golfer tournament scores info into "golferTournScores.csv"
           255 records in this format:
           golfer_tourn_id, tourn_id, golfer_id
           total_tourn_score, round1_score, ..., round4_score

        8. tournament scores info into "tournScores.csv"
           15 records in this format:
           tourn_scores_id, tourn_id, top_tourn_score,
           top_round1_score, ..., top_round4_score

    The functions reading in the data return lists:
        readGolfCourses
        readGolfers
        readTournaments
        readRoundScores

    These lists are used to create eight files containing database
    table information using these functions:
        createGolfCourse: courses
        createHoles: holes
        createGolfers: golfers
        createTournaments: tournaments
        createRounds: rounds
        createGolferRoundScores: golfer_round_scores
        createGolferTournScores: golfer_tourn_scores
        createTournScores: all_tourn_scores

    Other functions:
    writeFile()
    findWinners(): extra credit
    """

    print("Wake Golf Tour\n")

    # File names for input

    golf_courses_infile = "golfCoursesInput.csv"
    golfers_infile = "golfersInput.csv"
    tournaments_infile = "tournamentsInput.csv"
    rounds_infile = "roundScoresInput.csv"

    # File names for output

    golf_courses_file = "golfCourses.csv"
    holes_file = "holes.csv"
    golfers_file = "golfers.csv"
    tournaments_file = "tournaments.csv"
    rounds_file = "rounds.csv"
    golfer_round_scores_file = "golferRoundScores.csv"
    golfer_tourn_scores_file = "golferTournScores.csv"
    tourn_scores_file = "tournScores.csv"

    # Read golf course input file
    # Create golf course entity records
    # Create holes entity records

    courses_list = readGolfCourses(golf_courses_infile)
    golf_courses = createGolfCourse(courses_list)
    holes = createHoles(golf_courses)

    # Read golfers input file
    # Create golfers entity records

    golfers_list = readGolfers(golfers_infile)
    golfers = createGolfers(golfers_list)

    # Read tournaments input file
    # Create tournaments entity records
    # Create rounds entity records

    tourns_list = readTournaments(tournaments_infile)
    tournaments = createTournaments(tourns_list, golfers, golf_courses)
    rounds = createRounds(tournaments)

    # Read round scores input file
    # Create golfer round scores entity records
    # Create golfer tourn scores entity records

    scores_list = readRoundScores(rounds_infile)
    golfer_round_scores = createGolferRoundScores(scores_list, golfers, tournaments, rounds)
    golfer_tourn_scores = createGolferTournScores(golfer_round_scores, tournaments)
    all_tourn_scores = createTournScores(golfer_tourn_scores, tournaments)
    findWinners(all_tourn_scores, golfer_tourn_scores, golfers)

    # Write out new tables

    writeFile(golf_courses_file, golf_courses)
    writeFile(holes_file, holes)
    writeFile(golfers_file, golfers)
    writeFile(tournaments_file, tournaments)
    writeFile(rounds_file, rounds)
    writeFile(golfer_round_scores_file, golfer_round_scores)
    writeFile(golfer_tourn_scores_file, golfer_tourn_scores)
    writeFile(tourn_scores_file, all_tourn_scores)


def readGolfCourses(filename):
    """
    golf_course, par_h1, par_h2, ..., par_h18

    Algorithm:
    Each line (golf course data) is read and placed in a course list,
         using the string split method.
    The first element is stripped of whitespace.
    The rest of the elements (par values) are converted to a int.
    Each course list is appended to a larger coursesList
        and the coursesList is returned.
    Use a try/except block to capture a File Not Found Error
    """
    courses_list = []

    print("Golf Courses List:")

    try:
        input_file = open(filename, 'r')
        for line in input_file:
            golf_course = line.split(",")

            golf_course[0] = golf_course[0].strip()
            for i in range(18):
                golf_course[i + 1] = int(golf_course[i + 1])
            courses_list.append(golf_course)

    except IOError:
        print("File Not Found Error.")

    input_file.close()
    #print(courses_list)
    return courses_list


def createGolfCourse(courses_list):
    """
    Use courses_list
    course_name, par_h1, par_h2, ..., par_h18

    Convert to
    course_id, course_name, total_par, par_h1, par_h2, ..., par_h18
    """
    print("Golf Courses:")

    golf_courses = []

    course_id = 1
    for course in courses_list:
        golf_course = []
        golf_course.append(course_id)
        golf_course.append(course[0])
        golf_course.append(sum(course[1:]))
        golf_course.append(course[1:])
        course_id += 1
        golf_courses.append(golf_course)

    #print(golf_courses)
    return golf_courses


def createHoles(golf_courses):
    """
    Use courses
    course_id, course_name, total_par, par_h1, par_h2, ..., par_h18

    Convert to
    hole_id, course_id, hole_num, par
    """
    print("Holes:")

    holes = []
    hole_id = 1

    # Add the code here to finish this function
    for courses in golf_courses:
        for h in range(1, 19):
            hole = []

            hole.append(hole_id)
            hole.append(courses[0])  # course_id
            hole.append(h) # hole number
            hole.append(courses[3][h-1])  # par

            hole_id += 1
            holes.append(hole)

    #print(holes)
    return holes


def readGolfers(filename):
    """
    golfer1_name
    ...
    golfer30_name

    Algorithm:
    Each line (golfer name) is read, the whitespace stripped,
        and appended in a golfers_list
    Use a try/except block to capture a File Not Found Error
    """
    golfers_list = []

    print("Golfers List:")

    # Add the code here to finish this function
    try:
        input_file = open(filename, 'r')
        for line in input_file:
            golfer_name = line.strip()
            golfers_list.append(golfer_name)  # get golfers name

    except IOError:
        print("File Not Found Error.")
    #print(golfers_list)
    return golfers_list


def createGolfers(golfers_list):
    """
    Use golfers_list
    golfer_name

    Convert to
    golfer_id, golfer_name
    """
    print("Golfers with ID's:")
    golfers = []

    # Add the code here to finish this function

    golfer_id = 1
    for gf in golfers_list:
        golfer = []
        golfer.append(golfer_id)
        golfer.append(gf)
        golfer_id += 1
        golfers.append(golfer)

    print(golfers)
    return golfers


def readTournaments(filename):
    """
    Each tournament covers two record types in the file.
    The first record has
        golf_course, tournament, start_date, num_rounds, num_golfers
    The rest of records have
        golfer's names on a separate lines

    Algorithm:
    For each tournament
        The first line is read and placed in a tourn_header list,
            using the string split method.
        The first three elements are stripped of whitespace.
        The last two elements are converted to a int.
        Loop to read the next num_golfers lines, strip of whitespace,
            and append to golfer_list
        Concatenate tourn_header to golfer_list into tournament
        Append tournament to tourns_list
    Return tourns_list
    Use a try/except block to capture a File Not Found Error
    """
    tourns_list = []
    golfer_list = []

    print("Tournament List:")

    try:
        input_file = open(filename, 'r')
        rec = 0
        for line in input_file:
            if rec == 0:
                tourn_header = line.split(",")
                for i in range(3):
                    tourn_header[i] = tourn_header[i].strip()
                for j in range(2):
                    tourn_header[j + 3] = int(tourn_header[j + 3])
                num_golfers = tourn_header[4]
                golfer_list.clear()
                rec = num_golfers
            else:
                line = line.strip()
                golfer_list.append(line)
                rec -= 1
                if rec == 0:
                    tournament = tourn_header + golfer_list
                    tourns_list.append(tournament)

    except IOError:
        print("File Not Found Error.")

    input_file.close()
    #print(tourns_list, "Golfer List:", golfer_list)
    return tourns_list


def createTournaments(tourns_list, golfers, golf_courses):
    """
    Use tourns_list:
    golf_course, tourn_name, start_date, num_rounds, num_golfers,
    golfer_name1, golfer_name2, ..., golfer_name15

    Use golfers:
    golfer_id, golfer_name

    Use golf_courses:
    course_id, course_name, total_par, par_h1, par_h2, ..., par_h18

    Convert to
    tourn_id, tourn_name, course_id, start_date, num_rounds,
    num_golfers, golfer_id1, golfer_id2, ..., golfer_id15

    """
    print("Tournaments:")

    tournaments = []
    tid = 1  # tourn_id

    for tourn in tourns_list:
        tournament = []
        tournament.append(tid)  # tourn_id
        tournament.append(tourn[1])  # tourn_name

        for course in golf_courses:  # Find course_id
            if course[1] == tourn[0]:  # Match course_name
                tournament.append(course[0])  # course_id

        tournament.append(tourn[2])  # start_date
        tournament.append(tourn[3])  # num_rounds
        tournament.append(tourn[4])  # num_golfers

        for golfer in tourn[5:]:  # Find golfer_id for golfers
            for player in golfers:  # that played in tournament
                if player[1] == golfer:  # Match names
                    tournament.append(player[0])  # golfer_id

        tournaments.append(tournament)  # Add to outer list

        tid = tid + 1  # tourn_id
    print(tournaments)
    return tournaments


def createRounds(tournaments):
    """
    Use tournaments
    tourn_id, tourn_name, course_id, start_date, num_rounds,
    num_golfers, golfer_id1, golfer_id2, ... golfer_id15,

    Convert to

    round_id, tourn_id, day
    """
    print("Rounds:")

    rounds = []

    rid = 1

    for tourn in tournaments:
        num_rounds = tourn[4]
        for r in range(tourn[4]):  # num_rounds
            round = []
            round.append(rid)  # round_id

            round.append(tourn[0])  # tourn_id

            if num_rounds == 4:
                day = "Thu"
            elif num_rounds == 3:
                day = "Fri"
            elif num_rounds == 2:
                day = "Sat"
            elif num_rounds == 1:
                day = "Sun"
            round.append(day)  # day

            rounds.append(round)  # Add to outer list

            num_rounds = num_rounds - 1
            rid = rid + 1  # round_id
    print(rounds)
    return rounds


def readRoundScores(filename):
    """
    golfer_name, tourn_name, day, hole1, hole2, ..., hole18

    Algorithm:
    Each line (round scores data) is read and placed in a scores list,
         using the string split method.
    The first three elements are stripped of whitespace.
    The rest of the elements (hole scores) are converted to a int.
    Each scores list is appended to a larger golf_scores
        and the golf_scores is returned.
    Use a try/except block to capture a File Not Found Error
    """
    print("Golf Scores List:")

    golf_scores = []

    try:
        input_file = open(filename, 'r')
        for line in input_file:
            golf_score = line.split(",")

            golf_score[0] = golf_score[0].strip() # golfer name
            golf_score[1] = golf_score[1].strip() # tournament
            golf_score[2] = golf_score[2].strip() # day

            for i in range(18):
                golf_score[i + 3] = int(golf_score[i + 3]) # golfer scores(18 ints)
            golf_scores.append(golf_score)

    except IOError:
        print("File Not Found Error.")

    input_file.close()
    print(golf_scores)
    return golf_scores


def createGolferRoundScores(golf_scores, golfers, tournaments, rounds):
    """
    Use golf_scores
    golfer_name, tourn_name, day, hole1, hole2, ..., hole18

    Use golfers
    golfer_id, golfer_name

    Use tournaments
    tourn_id, tourn_name, course_id, start_date, num_rounds,
    num_golfers, golfer_id1, golfer_id2, ... golfer_id15,

    Use rounds
    round_id, tourn_id, day

    Convert to
    golfer_round_id, tourn_id, round_id, golfer_id,
    total_round_score, hole1_score, hole2_score, ..., hole18_score
    """
    print("Golfer Round Scores:")

    golfer_round_scores = []

    # Add the code here to finish this function
    gr_id = 1
    for scores in golf_scores:
        golfer_round = []
        golfer_round.append(gr_id)  # golfer round id
        gr_id += 1

        for tourns in tournaments:
            if scores[1] == tourns[1]:
                tourn_id = tourns[0]
                golfer_round.append(tourn_id) # tourn_id

        for round in rounds:
            if tourn_id == round[1]:
                if scores[2] == round[2]:
                    round_id = round[0]
                    golfer_round.append(round_id) # round_id

        for golfer in golfers:
            if golfer[1] == scores[0]:
                golfer_round.append(golfer[0]) # golfer_id)
                golfer_round.append(sum(scores[3:])) # golfer total par per course
                golfer_round.extend(scores[3:]) # golfer scores per hole per course

        golfer_round_scores.append(golfer_round)

    print(golfer_round_scores)
    return golfer_round_scores
#createGolferRoundScores(readRoundScores("roundScoresInput.csv"), createGolfers(readGolfers("golfersInput.csv")), createTournaments(readTournaments("tournamentsInput.csv"), createGolfers(readGolfers("golfersInput.csv")), createGolfCourses("golfCoursesInput.csv"))), createRounds(createTournaments(readTournaments("tournamentsInput.csv"), createGolfers(readGolfers("golfersInput.csv")), createGolfCourse(readGolfCourses("golfCoursesInput.csv")))))


def createGolferTournScores(golfer_round_scores, tournaments):
    """
    Use golfer_round_scores
    golfer_round_id, tourn_id, round_id, golfer_id,
    total_round_score, hole1_score, hole2_score, ..., hole18_score

    Use tournaments
    tourn_id, tourn_name, course_id, start_date, num_rounds,
    num_golfers, golfer_id1, golfer_id2, ..., golfer_id15

    Convert to
    golfer_tourn_id, tourn_id, golfer_id,
    total_tourn_score, round1_score, round2_score, .., round4_score
    """

    print("Golfer Tournament Scores:")

    golfer_tourn_scores = []
    gtid = 1

    for tourn in tournaments:
        num_golfers = tourn[5]  # num_golfers
        tourn_id = tourn[0]  # tourn_id
        num_rounds = tourn[4]  # num_rounds

        for gind in range(num_golfers):  # number of golfers
            golfer_scores = []

            golfer_id = tourn[gind + 6]  # golfer_id

            golfer_scores.append(gtid)  # golfer_tourn_id
            golfer_scores.append(tourn_id)  # tourn_id
            golfer_scores.append(golfer_id)  # golfer_id

            round_totals = [0]
            for scores in golfer_round_scores:
                if scores[1] == tourn_id:  # Match tourn_id
                    if scores[3] == golfer_id:  # Match golfer_id
                        round_totals.append(scores[4])

            for i in range(4 - num_rounds):  # Place zero scores  for
                round_totals.append(0)  # tourns with < 4 rounds

            tourn_total = sum(round_totals)  # Get sum of rounds
            round_totals[0] = tourn_total  # Place at top of list

            golfer_scores = golfer_scores + round_totals

            golfer_tourn_scores.append(golfer_scores)  # Add to outer list

            gtid = gtid + 1
    print(golfer_tourn_scores)
    return golfer_tourn_scores


def createTournScores(golfer_tourn_scores, tournaments):
    """
    Use golfer_tourn_scores
    golfer_tourn_id, tourn_id, golfer_id, total_tourn_score,
    round1_score, round2_score, round3_score round4_score

    Use tournaments
    tourn_id, tourn_name, course_id, start_date, num_rounds,
    num_golfers, golfer_id1, golfer_id2, ..., golfer_id15

    Convert to
    tourn_scores_id, tourn_id, top_tourn_score,
    top_round1_score, top_round2_score, top_round2_score, top_round4_score
    """

    print("Top Tournament Scores:")

    all_tourn_scores = []
    tsid = 1
    for tourn in tournaments:
        top_scores = [999, 999, 999, 999, 999]  # Used to hold the current
        # lowest score for
        tourn_scores = []  # tournments and rounds

        tourn_id = tourn[0]  # tourn id
        tourn_scores.append(tsid)  # tourn_scores_id
        tourn_scores.append(tourn_id)  # tourn_id

        for golfer_scores in golfer_tourn_scores:
            if golfer_scores[1] == tourn_id:  # Match the tournament IDs

                for r in range(5):
                    if golfer_scores[r + 3] < top_scores[r]:
                        top_scores[r] = golfer_scores[r + 3]

        for s in range(5):
            tourn_scores.append(top_scores[s])

        all_tourn_scores.append(tourn_scores)

        tsid = tsid + 1
    print(all_tourn_scores)
    return all_tourn_scores


def writeFile(filename, table):
    output_file = open(filename, 'w')
    for record in table:
        strRec = ''
        for field in record:
            strRec = strRec + str(field) + ','
        strRec = strRec.rstrip(',') + '\n'
        output_file.write(strRec)

    output_file.close()

def findWinners (all_tourn_scores, golfer_tourn_scores, golfers):
    print ("Extra Credit To Code This One And Display The Winners of Each Tournament")
    winners = []

    for tourn in all_tourn_scores:
        tourn_winner = []

        for tourn_score in golfer_tourn_scores:

            if tourn[1] == tourn_score[1] and tourn[2] == tourn_score[3]: # find if tourn_id and scores are equal
                tourn_winner.append(tourn_score[1]) # append tournament id to inner list
                golfer_id = tourn_score[2]
                total_score = tourn_score[3]


                for golfer in golfers:

                    if golfer_id == golfer[0]:
                        golfer_name = golfer[1]
                        tourn_winner.append(golfer_name)
                        tourn_winner.append(total_score)

                        winners.append(tourn_winner)

    print(winners)

main()