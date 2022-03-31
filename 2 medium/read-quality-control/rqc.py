import gzip
from collections import Counter
from pathlib import Path


class DataRead:
    filepath: Path
    data: list[str]

    data_len: int
    avg_len: float
    repeats: int
    n_reads: int
    gc_avg: float
    n_avg: float

    def __init__(self, filepath: str, analyze: bool = True) -> None:
        self.filepath = Path(filepath)
        if self.filepath.suffix == ".gz":
            with gzip.open(self.filepath, mode="rt") as file:
                self.data = file.read().splitlines()[1::4]
        else:
            with open(self.filepath) as file:
                self.data = file.read().splitlines()[1::4]

        if analyze:
            self.analyze()

    def analyze(self) -> None:
        self.data_len = sum(len(d) for d in self.data)
        self.avg_len = round(self.data_len / len(self.data))

        repeats = Counter(self.data)
        self.repeats = sum(repeats.values()) - len(repeats)

        self._analyze_contents()

    def present(self) -> None:
        print("Reads in the file", len(self.data))
        print("Reads sequence average length =", self.avg_len)
        print("\nRepeats =", self.repeats)
        print("Reads with Ns =", self.n_reads)
        print(f"\nGC content average = {self.gc_avg}%")
        print(f"Ns per read sequence = {self.n_avg}%")

    def _analyze_contents(self) -> None:
        gc_avg, n_avg, self.n_reads = [], [], 0

        for d in self.data:
            gc, n = 0, 0

            for base in d:
                if base in "GC":
                    gc += 1
                elif base in "N":
                    n += 1

            gc_avg.append(round(gc / len(d) * 100, 2))
            n_avg.append(round(n / len(d) * 100, 2))
            self.n_reads += bool(n)

        self.gc_avg = round(sum(gc_avg) / len(gc_avg), 2)
        self.n_avg = round(sum(n_avg) / len(n_avg), 2)


if __name__ == "__main__":
    reads = [DataRead(input()) for _ in range(3)]
    min(reads, key=lambda x: x.repeats + x.n_reads).present()
