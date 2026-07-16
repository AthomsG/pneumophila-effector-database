# Catalogue quality audit

Audit date: 2026-07-16. This assessment examines the 1,303 records currently emitted by the pipeline and the raw records that caused their inclusion.

## Verdict

The current master file is **not yet a defensible list of all known *Legionella* effectors**. It is a useful high-recall discovery set containing three different things:

1. a strong *L. pneumophila* reference set derived from reported Dot/Icm-dependent translocation screens;
2. automatically annotated or inferred effector homologues from 65 taxa;
3. clear text-query false positives and source-mapping errors.

Those groups need to be separated before the main FASTA can be described as “known effectors.”

## What is in the current file

| Observation | Count |
|---|---:|
| Total master records | 1,303 |
| Records contributed by Pathogens3D | 368 |
| UniProt-only records | 935 |
| Curated annotation | 24 |
| Automated annotation | 945 |
| Ambiguous candidate | 334 |
| Distinct taxonomy IDs | 65 |
| Records included through explicit effector/Dot-Icm wording somewhere in UniProt | 829 |
| Records included through Pathogens3D without equivalent explicit UniProt wording | 342 |
| Records included only by matching a known name | 132 |

The large number of species and strain homologues explains why the catalogue is much larger than the roughly 368-effectors repertoire usually discussed for *L. pneumophila*. This is not inherently wrong, but it answers a different question: “proteins across the genus annotated or inferred to resemble effectors,” rather than “known effectors.”

## Clear false positives

At least **142 records are identifiable as high-confidence noise from their product names alone**. The categories below are mutually exclusive in the current data.

| Noise mechanism | Count | Examples |
|---|---:|---|
| Conserved gene-name collisions | 90 | 62 elongation factor 4 proteins named `lepA`, 27 signal peptidase I proteins named `lepB`, and one daunorubicin-resistance ATPase named `drrA` |
| “Effector-binding/domain” text unrelated to a translocated Dot/Icm effector | 23 | AraC effector-binding proteins and SMODS/SLOG effector-domain proteins |
| Effectors of other secretion systems | 20 | type II, type III, and type VI secretion effectors |
| Dot/Icm apparatus, adapter, or coupling proteins | 9 | DotL, DotM, DotN, DotY, DotZ, IcmS, IcmW, and LvgA |

The apparatus proteins are especially instructive: their reviewed UniProt comments discuss interaction with effectors, and the current full-record text test mistakes that discussion for evidence that the apparatus component is itself an effector.

Name matching is unsafe without biological disambiguation. `LepA` and `LepB` are established effector names, but they are also widely used names for housekeeping elongation factor 4 and signal peptidase I. Similarly, the word “effector” has meanings in transcription-regulator and toxin-domain annotations that are unrelated to Dot/Icm translocation.

## How strong is Pathogens3D?

Pathogens3D is the strongest discovery source currently used, not merely optional annotation. Its associated study describes a set of 368 *L. pneumophila* proteins compiled from previously reported genome-wide tests of Dot/Icm-dependent host-cell translocation. That is substantially better provenance than an automatically propagated UniProt product name. The study deliberately includes proteins whose molecular functions remain unknown: in the downloaded table, 218 of 368 have the protein description “Uncharacterized protein,” while every row has a structural/domain annotation.

This distinction matters: experimental support for **translocation** does not imply experimental knowledge of **molecular function**. The current single evidence field cannot express that distinction and incorrectly labels most Pathogens3D-only entries `ambiguous_candidate`.

Sources: [Pathogens3D Legionella page](https://pathogens3d.org/legionella-pneumophila) and [the associated 368-effector structural atlas](https://pmc.ncbi.nlm.nih.gov/articles/PMC11696984/).

Pathogens3D accession mappings also require validation:

- `lpg2434` is mapped to `A0A3N9YH02`, an *Aeromonas caviae* protein. Querying the *L. pneumophila* locus identifies `Q5ZST2` instead.
- `lpg2628` is mapped to inactive accession `A0A077GS41`. Querying the strain and locus identifies active accession `Q5ZS91`.

The builder currently trusts the supplied accessions and therefore emits one non-*Legionella* record and one sequence-less inactive record.

## What remains uncertain after removing obvious noise

Removing the 142 obvious false positives would not make every remaining record “known.” Most UniProt-only hits are unreviewed strain/species homologues with generic names such as “Dot/Icm T4SS effector.” These are plausible candidates, but a product name propagated by an annotation pipeline is not independent experimental evidence of translocation.

Conversely, restricting the catalogue to reviewed UniProt entries would be far too conservative. Only 24 current records are categorized as curated, while the translocation-screen-derived *L. pneumophila* set contains hundreds of valid proteins that UniProt still describes as uncharacterized.

UniProt alone is therefore insufficient for a high-recall known-effector catalogue. Pathogens3D, its underlying publications, and manual literature curation should define the known seed set; UniProt should supply current sequence and metadata and discover homologues.

## Recommended catalogue design

1. Define the primary FASTA as a reference set of effectors with explicit provenance for Dot/Icm-dependent translocation. Begin with the Pathogens3D 368-protein set, repair its accession mappings by strain plus locus tag, and add literature-supported records manually.
2. Keep inferred homologues in a separate candidate/homologue output. Do not mix them into the known-effector FASTA merely because UniProt contains “effector” in an automated name.
3. Replace the single evidence category with separate fields such as `translocation_evidence`, `functional_evidence`, and `annotation_status`. A protein may have experimental translocation support but an unknown function.
4. Restrict automated discovery to Dot/Icm-specific wording and explicit known-effector products. Reject apparatus components, other secretion systems, “effector-binding/domain” products, and housekeeping-name collisions.
5. Validate every source accession against genus, strain, locus tag, and sequence length. Fall back to a strain-and-locus UniProt lookup when an accession is inactive or taxonomically inconsistent.
6. Preserve all broad-query hits only in ignored diagnostics so search sensitivity can still be audited without presenting those hits as biological truth.

The most defensible immediate main product is therefore a corrected, provenance-rich *L. pneumophila* reference repertoire. A genus-wide “all known *Legionella* effectors” file requires an explicit policy for whether strain homologues count as separate known effectors and what level of translocation evidence is required.

