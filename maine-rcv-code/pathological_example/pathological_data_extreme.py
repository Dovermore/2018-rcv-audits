import os
from audit_me import audit

if __name__ == "__main__":
    num_candidates = 10

    actual_winner_vote = 5000
    actual_loser_vote = 2499
    actual_cross_vote = 2500
    # hi = actual_winner_vote + actual_loser_vote + \
    #       (num_candidates - 2) * actual_cross_vote - 9
    # lo = hi - 8000
    step = 4000

    hi = actual_winner_vote + actual_loser_vote + \
            (num_candidates - 2) * actual_cross_vote
    lo = hi

    # actual_winner_vote = 100
    # actual_loser_vote = 50
    # actual_cross_vote = 49
    # lo = 10
    # hi = 190
    # step = 10

    data_file = f"actual_{num_candidates:03}{actual_winner_vote:05}" \
        f"{actual_loser_vote:05}{actual_cross_vote:05}.csv"
    tmp_file = f"audit_actual_{num_candidates:03}{actual_winner_vote:05}" \
        f"{actual_loser_vote:05}{actual_cross_vote:05}.csv.tmp"
    add_to_file = f"audit_actual_{num_candidates:03}{actual_winner_vote:05}" \
        f"{actual_loser_vote:05}{actual_cross_vote:05}.csv"

    audit(1000, os.getcwd(), data_file, output_file=tmp_file,
          lo=lo, hi=hi, step=step)

    with open(add_to_file, "r") as add_file:
        index = len(add_file.readlines()) - 1

    with open(tmp_file, "r") as tmp:
        with open(add_to_file, "a") as add_file:
            for line in tmp.readlines()[1:]:
                # Reindex the file
                split = line.split(",", 1)
                line = str(index) + "," + split[1]
                index += 1
                add_file.write(line)
