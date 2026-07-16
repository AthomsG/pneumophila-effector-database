# Pangenome embedding-cluster assessment

Assessment date: 2026-07-16. Input: `selection-1784214596141.json`, a 567-family selection exported from the *L. pneumophila* pangenome embedding atlas.

## Result

The selected UMAP neighborhood is strongly enriched for known effector families, but embedding proximity is candidate-generating evidence rather than experimental validation.

| Metric | Value |
|---|---:|
| Selected pangenome families | 567 |
| Already labelled as effectors | 268 |
| Unlabelled selected families | 299 |
| Positive fraction inside selection | 47.3% |
| Positive families visible in the complete atlas | 407 / 9,115 (4.5%) |
| Approximate enrichment in selection | 10.6-fold |
| Fraction of all labelled atlas families captured by selection | 65.8% |

The neighborhood therefore has useful biological signal, but it is neither pure nor exhaustive. About half the selected families are not labelled effectors, and 139 labelled effector families lie outside the selection.

## Likely mapping misses among the 299 unlabelled families

Forty unlabelled families have annotations that explicitly describe a Dot/Icm effector/substrate or identify a known effector family/domain. High-frequency examples include:

| Pangenome family | Frequency | Length (aa) | Annotation |
|---|---:|---:|---|
| `group_1018` | 97.128% | 282 | Glycosyl transferase; Dot/Icm secretion system substrate |
| `group_2864` | 71.453% | 185 | Dot/Icm secretion system substrate |
| `group_2745` | 69.257% | 370 | Dot/Icm secretion system substrate; secreted protein |
| `group_2024` | 58.868% | 487 | Dot/Icm T4SS effector |
| `group_127` | 58.277% | 238 | Dot/Icm secretion system substrate |
| `sdeC` | 49.071% | 674 | SdeC protein substrate of the Dot/Icm system |
| `group_2842` | 47.720% | 586 | Dot/Icm T4SS effector |
| `group_2806` | 40.541% | 272 | Dot/Icm T4SS effector |
| `group_2981` | 35.389% | 250 | Dot/Icm T4SS effector |
| `group_116` | 28.294% | 1,096 | Dot/Icm T4SS effector |
| `drrA` | 21.115% | 624 | DrrA phosphatidylinositol-4-phosphate-binding domain protein |
| `group_3088` | 20.693% | 1,004 | SidE PDE domain-containing protein |
| `group_5239` | 17.821% | 1,069 | Dot/Icm T4SS effector |
| `group_1184` | 16.807% | 1,067 | Dot/Icm T4SS effector |
| `group_240` | 9.713% | 880 | SidC N-terminal domain-containing protein |

These are not necessarily 40 newly discovered effectors. Several are probably alternate pangenome families, fragments, paralogues, or divergent homologues of effectors already represented by Pathogens3D. For example, the export separately contains unlabelled `drrA`, `sdeC`, `sidE`, and SdeC-like families even though those effector systems are already established.

Another 41 unlabelled families contain effector-associated but non-specific architectures such as ankyrin repeats, F-boxes, U-boxes, leucine-rich repeats, or protein-kinase domains. These features raise priority for investigation but are not sufficient for inclusion: such domains also occur in non-effector proteins.

The neighborhood also contains obvious non-effectors, including Cas9, integral membrane proteins, transport-related proteins, and the DotY secretion apparatus component. This confirms that local UMAP membership cannot serve as a positive label.

## What is needed to resolve the candidates

The JSON contains family summaries, annotations, coordinates, and the existing effector label, but no representative amino-acid sequence, member locus tags, genome identifiers, or nearest-neighbor distances. Consequently it is not possible to establish whether an unlabelled family is:

- an exact or near-exact match missed by the original mapping threshold;
- a fragment or paralogue of a Pathogens3D protein;
- a divergent homologue in another strain;
- or a genuinely novel candidate.

The next comparison needs the representative protein FASTA used for embedding plus a family-to-member table. Each candidate should then be searched against the established reference with sequence coverage and identity reported in both directions. Candidate status should remain separate from the established database unless a publication provides experimental Dot/Icm translocation evidence.

## Inclusion policy

- **Established reference:** add only with a publication demonstrating or reporting Dot/Icm-dependent translocation; record DOI/PMID and the exact strain/locus/accession.
- **Known-family homologue:** useful for pangenome analysis but not a new established effector; store outside the primary reference and link it to the established family.
- **Embedding candidate:** retain for prioritization and experimental/literature follow-up; never use as a training positive solely because it clusters with effectors.

For a future EffectorPredictor, the established reference is suitable as a positive seed only after sequence clustering and homology-aware data splitting. Random sequence-level splits would leak close pangenome homologues between training and evaluation and substantially inflate performance.

