from dataclasses import InitVar, dataclass, field
from statistics import mean
from typing import Iterable

exams: tuple = ("Physics", "Chemistry", "Mathematics", "Computer Science", "Special")
exams_by_dep: dict[str, tuple] = {
    "Biotech": ("Chemistry", "Physics"),
    "Chemistry": ("Chemistry",),
    "Engineering": ("Computer Science", "Mathematics"),
    "Mathematics": ("Mathematics",),
    "Physics": ("Physics", "Mathematics"),
}


@dataclass
class Applicant:
    data: InitVar[str]
    name: str = field(init=False)
    exams: dict[str, int] = field(init=False)
    priorities: list[str] = field(init=False)
    dep_scores: dict[str, float] = field(default_factory=dict, init=False)

    def __post_init__(self, data: str):
        data, *priorities = data.strip().rsplit(maxsplit=3)
        self.name, *scores = data.rsplit(maxsplit=len(exams))
        self.priorities = priorities
        self.exams = dict(zip(exams, map(int, scores)))
        for dep in exams_by_dep:
            try:
                self.dep_scores[dep] = self._dep_score(dep)
            except KeyError:
                continue

    def _dep_score(self, dep: str) -> float:
        return mean(self.exams[ex] for ex in exams_by_dep[dep])


def load_applicants(filename: str) -> list[Applicant]:
    with open(filename) as f:
        return [Applicant(line) for line in f.readlines()]


def sort_applicants(
    applicants: Iterable[Applicant], dep: None | str = None
) -> list[Applicant]:
    return (
        sorted(
            applicants,
            key=lambda a: (-max(a.dep_scores[dep], a.exams["Special"]), a.name),
        )
        if dep is not None
        else sorted(applicants, key=lambda a: a.name)
    )


def show_accepted_applicants(applicants: dict[str, list[Applicant]]) -> None:
    for dep, students in applicants.items():
        print(f"\n{dep}", *[s.name for s in students], sep="\n")


def save_accepted_applicants(applicants: dict[str, list[Applicant]]) -> None:
    for dep, students in applicants.items():
        with open(f"{dep.lower()}.txt", "w") as f:
            f.writelines(
                f"{s.name} {max(s.dep_scores[dep], s.exams['Special'])}\n"
                for s in students
            )


if __name__ == "__main__":
    capacity: int = int(input())
    all_applicants: list = sort_applicants(load_applicants("applicants.txt"))
    dep_accepted: dict[str, list] = {dep: list() for dep in exams_by_dep}

    for wave in range(3):
        accepted: list = [s for students in dep_accepted.values() for s in students]
        pending: list = [a for a in all_applicants if a not in accepted]
        for dep in dep_accepted:
            eligible: filter = filter(
                lambda a: dep == a.priorities[wave] and dep in a.dep_scores, pending
            )
            for a in sort_applicants(eligible, dep):
                if len(dep_accepted[dep]) < capacity:
                    dep_accepted[dep].append(a)
                else:
                    break

    by_score = {dep: sort_applicants(dep_accepted[dep], dep) for dep in dep_accepted}
    show_accepted_applicants(by_score)
    save_accepted_applicants(by_score)
