def complement(orig):
    table = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join([table[base] for base in orig])


def cut(strand, site, comp=False):
    idx = strand.index(site)
    shift = len(site) - 1 if comp else 1
    return strand[: idx + shift], strand[idx + shift :]


def trim(strand, lsite, rsite, comp=False):
    cut_left = cut(strand, lsite, comp=comp)[1]
    return cut(cut_left, rsite, comp=comp)[0]


def insert(lfirst, rfirst, lfirst_comp, rfirst_comp, second, second_comp):
    return "".join(
        [
            lfirst,
            second,
            rfirst,
            "\n",
            lfirst_comp,
            second_comp,
            rfirst_comp,
        ]
    )


if __name__ == "__main__":
    with open(input()) as f:
        plasmid, plasmid_site, gfp, gfp_sites = f.read().splitlines()
        gfp_lsite, gfp_rsite = gfp_sites.split()

    lplasmid, rplasmid = cut(plasmid, plasmid_site)
    lplasmid_comp, rplasmid_comp = cut(
        complement(plasmid), complement(plasmid_site), comp=True
    )

    gfp_trim = trim(gfp, gfp_lsite, gfp_rsite)
    gfp_comp_trim = trim(
        complement(gfp), complement(gfp_lsite), complement(gfp_rsite), comp=True
    )

    print(
        insert(
            lplasmid, rplasmid, lplasmid_comp, rplasmid_comp, gfp_trim, gfp_comp_trim
        )
    )
