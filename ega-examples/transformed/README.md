# Transformed GHGA-compatible EGA JSON

This folder consists of EGA metadata JSON transformed from [../original]().

To transform the original JSON to a GHGA compatible form:

```sh
python ../../scripts/translate_ega_to_ghga.py \
    --ega-dac-json ../original/dacs.json \
    --ega-dataset-json ../original/datasets.json \
    --ega-studies-json ../original/studies.json
```
