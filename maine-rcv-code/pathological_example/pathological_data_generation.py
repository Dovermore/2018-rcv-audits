import os
from os import path
import csv


class PathologicalVoteGenerator:
    def __init__(self, num_candidates, winner_vote=500,
                 loser_vote=249, cross_vote=250):
        assert num_candidates > 3
        self.num_candidates = num_candidates
        self.winner_vote = winner_vote
        self.loser_vote = loser_vote
        self.cross_vote = cross_vote

    def __call__(self, file_name, output_dir="."):
        self.file_name = file_name
        self.output_dir = output_dir
        self.full_file_dir = path.join(output_dir, file_name)

        winner_vote = self.winner_vote
        loser_vote = self.loser_vote
        cross_vote = self.cross_vote

        if not path.exists(output_dir):
            os.makedirs(output_dir)

        candidates = ([f"A{i}" for i in range(self.num_candidates - 2)]
                      + ["B", "C"])

        with open(self.full_file_dir, "w") as file:
            file = csv.writer(file, quotechar='"')

            winner_ballot = ["C"]
            for i in range(winner_vote):
                file.writerow(winner_ballot)

            loser_ballot = ["B"]
            for i in range(loser_vote):
                file.writerow(loser_ballot)

            for i in range(cross_vote):
                for candidate in candidates[:-2]:
                    file.writerow([candidate, "B", "C"])


if __name__ == '__main__':
    num_candidates = 4

    actual_winner_vote = 5000
    actual_loser_vote = 2499
    actual_cross_vote = 2500

    reported_winner_vote = 4998
    reported_loser_vote = 4998
    reported_cross_vote = 4998

    pvg = PathologicalVoteGenerator(num_candidates,
                                    winner_vote=actual_winner_vote,
                                    loser_vote=actual_loser_vote,
                                    cross_vote=actual_cross_vote)
    actual_file = f"actual_{num_candidates:03}{actual_winner_vote:05}" \
        f"{actual_loser_vote:05}{actual_cross_vote:05}"
    pvg(actual_file+".csv")

    pvg = PathologicalVoteGenerator(num_candidates,
                                    winner_vote=reported_winner_vote,
                                    loser_vote=reported_loser_vote,
                                    cross_vote=reported_cross_vote)

    reported_file = f"reported_{num_candidates:03}{reported_winner_vote:05}" \
        f"{reported_loser_vote:05}{reported_cross_vote:05}"
    pvg(reported_file+".csv")

    from audit_me import audit

    audit(1000, os.getcwd(), actual_file+".csv",
          output_file=f"audit_{actual_file}.csv")
