# Transformed GHGA-compatible EGA JSON


To transform the [original EGA metadata JSON](../original) to a GHGA compatible form:

```sh
python ../../scripts/translate_ega_to_ghga.py \
    --ega-dac-json ../original/dacs.json \
    --ega-dataset-json ../original/datasets.json \
    --ega-studies-json ../original/studies.json \
    --embedded
```


**Note:** The files generated from the script will not be committed to the repo
due to their size.
